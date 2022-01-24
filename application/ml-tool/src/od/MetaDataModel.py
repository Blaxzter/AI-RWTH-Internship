import pickle
from typing import Dict, List, Callable, Optional

import numpy as np
from pyod.models.copod import COPOD
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.suod import SUOD
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

from src.Exceptions import NotInitializedException, FeatureAlreadyDefined
from src.od.metadata_features.ActionFeatures import ActionFeatures
from src.od.metadata_features.DateFeatures import DateFeatures
from src.od.metadata_features.GeneralFeatures import GeneralFeatures
from src.od.metadata_features.PathFeatures import PathFeatures
from src.od.metadata_features.UserFeatures import UserFeatures
from src.od.searchutils.FileTreeDatabase import FileTreeDatabase
from src.utils import Constants
from src.utils.Utils import weiben, get_outlier_probabilities


class MetaDataModel:

    def __init__(self, path_separator = "/", truncate_train_data = -1):

        self.unix_date_scaler = preprocessing.MinMaxScaler()
        self.path_separator = path_separator

        self.truncate_train_data = truncate_train_data
        self.feature_amount = -1

        self.initialized = False

        self.prev_action_data = None
        self.prev_file_tree = None
        self.file_database = FileTreeDatabase(path_separator = self.path_separator, add_user = True)

        self.feature_extractors = None
        self.feature_list = None
        self.feature_scalers = None
        self.decision_values = None

        self.trained_features = []
        self.clf = None

    def initialize_model(self, stored_data: Optional[Dict] = None):
        if stored_data:
            self.clf = pickle.loads(stored_data['model'])
            self.trained_features = stored_data[Constants.trained_features_dict_name]
            self.prev_action_data = stored_data[Constants.action_data_dict_name]

            prev_file_tree_json = stored_data[Constants.file_tree_dict_name]
            self.prev_file_tree = FileTreeDatabase(path_separator = self.path_separator)
            self.prev_file_tree.load_from_string(prev_file_tree_json)

            file_database_json = stored_data[Constants.file_database_dict_name]
            self.file_database = FileTreeDatabase(path_separator = self.path_separator, add_user = True)
            self.file_database.load_from_string(file_database_json)

            self.feature_extractors = self.create_feature_extractors(
                self.prev_file_tree, self.prev_action_data, self.file_database, self.path_separator
            )
            self.feature_list = self.get_feature_dict()
            self.feature_scalers = pickle.loads(stored_data[Constants.trained_scalers_dict_name])
        else:
            self.feature_extractors = self.create_feature_extractors(
                None, None, None, self.path_separator
            )
            self.feature_list = self.get_feature_dict()
            self.feature_scalers = {feature_name: StandardScaler() for feature_name in self.feature_list.keys()}
            # initialized a group of outlier detectors for acceleration
            detector_list = [LOF(n_neighbors = 15), LOF(n_neighbors = 20),
                             HBOS(n_bins = 10), HBOS(n_bins = 20),
                             COPOD(), IForest(n_estimators = 50),
                             IForest(n_estimators = 100),
                             IForest(n_estimators = 150)]
            # https://www.andrew.cmu.edu/user/yuezhao2/papers/21-mlsys-suod.pdf
            self.clf = SUOD(base_estimators = detector_list, n_jobs = 1, combination = 'average',
                            verbose = Constants.verbose_printing)

        self.feature_amount = len(self.feature_list)
        self.initialized = True

    def get_stored_model(self):
        return dict(
            model = pickle.dumps(self.clf),
            trained_features = self.trained_features,
            feature_scalers = pickle.dumps(self.feature_scalers),
            decision_values = self.decision_values,
            file_database = self.file_database.get_storable_elements(),
        )

    def fit(self, backup_data_list, ret_features = True):
        if not self.initialized:
            raise NotInitializedException('The meta data model is not initialized')

        processed_backup_data = self.parse_features_of_list(
            backup_data_list = backup_data_list, prev_backup_metadata = None, keep_prev_file_tree = ret_features
        )
        parsed_features = list(map(lambda x: x[Constants.backup_features_dict_name], processed_backup_data))
        self.trained_features = parsed_features
        train_matrix = self.vectorise(meta_data_feature_list = parsed_features, train = True)
        self.clf.fit(train_matrix)

        smallest_score = np.min(self.clf.decision_scores_).item()
        dec_threshold = self.clf.threshold_.item()
        biggest_score = np.max(self.clf.decision_scores_).item()
        self.decision_values = dict(
            smallest_score = smallest_score,
            dec_threshold = dec_threshold,
            biggest_score = biggest_score,
        )

        if ret_features:
            return processed_backup_data

    def re_predict(self):
        test_matrix = self.vectorise(self.trained_features, train = False)
        desc_boundary = self.clf.decision_function(test_matrix)
        prediction, confidence = self.clf.predict(test_matrix, return_confidence = True)
        outlier_probabilities = get_outlier_probabilities(desc_boundary, self.decision_values)
        return prediction.tolist(), confidence.tolist(), desc_boundary.tolist(), outlier_probabilities.tolist()

    def predict(self, backup_data_list, prev_backup_data, add_to_model = False, ret_backup_metadata = True):
        if not self.initialized:
            raise NotInitializedException('The meta data model is not initialized')

        processed_backup_data = self.parse_features_of_list(
            backup_data_list = backup_data_list, prev_backup_metadata = prev_backup_data,
            keep_prev_file_tree = ret_backup_metadata,
        )
        parsed_features = list(map(lambda x: x[Constants.backup_features_dict_name], processed_backup_data))
        test_matrix = self.vectorise(parsed_features, train = False)
        desc_boundary = self.clf.decision_function(test_matrix)
        prediction, confidence = self.clf.predict(test_matrix, return_confidence = True)

        outlier_probabilities = get_outlier_probabilities(desc_boundary, self.decision_values)

        if add_to_model:
            if Constants.verbose_printing:
                print('Meta Data Model continues training')
            # Add the new backup data to the trained model
            for backup_features in parsed_features:
                self.trained_features.append(backup_features)

            if self.truncate_train_data > 0:
                # Todo throw away oldest stored stuff
                pass

            train_matrix = self.vectorise(meta_data_feature_list = self.trained_features, train = True)
            self.clf.fit(train_matrix)

            smallest_score = np.min(self.clf.decision_scores_).item()
            biggest_score = np.max(self.clf.decision_scores_).item()
            dec_threshold = self.clf.threshold_.item()
            self.decision_values = dict(
                smallest_score = smallest_score,
                dec_threshold = dec_threshold,
                biggest_score = biggest_score,
            )

            # Add the paths to the backup data
            for backup_data in backup_data_list:
                self.file_database.add_backup_data(backup_data)

        if ret_backup_metadata:
            return prediction.tolist(), confidence.tolist(), desc_boundary.tolist(), outlier_probabilities.tolist(), processed_backup_data
        else:
            return prediction.tolist(), confidence.tolist(), desc_boundary.tolist(), outlier_probabilities.tolist()

    def vectorise(self, meta_data_feature_list: List[Dict], train = False):
        data_matrix = np.zeros((len(meta_data_feature_list), self.feature_amount))
        for idx, features in enumerate(meta_data_feature_list):
            data_array = []
            for name, feature in features.items():

                if train:
                    data_array.append(feature)
                else:
                    # Assume that the scaler are fitted as they are previously scaled
                    feature_scaler = self.feature_scalers.get(name)
                    to_transform = np.asarray([[feature]])
                    scaled_feature = feature_scaler.transform(to_transform)
                    data_array.append(scaled_feature.item())

            data_matrix[idx] = np.asarray(data_array)

        if train:
            # Go over each feature type and use a different scaler to scale independently
            for idx, (scaler_name, scaler) in enumerate(self.feature_scalers.items()):
                feature_data = data_matrix[:, idx]
                feature_data = feature_data.reshape(-1, 1)
                scaler.fit(feature_data)
                data_matrix[:, idx] = scaler.transform(feature_data).flatten()

        return data_matrix

    def parse_features_of_list(self, backup_data_list, prev_backup_metadata = None, keep_prev_file_tree = True):

        # Load data for initial run
        if prev_backup_metadata is None:
            self.file_database = FileTreeDatabase(path_separator = self.path_separator, add_user = True)
            self.feature_extractors = self.create_feature_extractors(None, None, self.file_database,
                                                                     self.path_separator)
        else:
            prev_action_data = prev_backup_metadata[Constants.action_data_dict_name]
            prev_file_tree = FileTreeDatabase(path_separator = self.path_separator)
            prev_file_tree.load_from_string(prev_backup_metadata[Constants.file_tree_dict_name])

            self.feature_extractors = self.create_feature_extractors(
                prev_file_tree, prev_action_data, self.file_database, self.path_separator
            )

        self.feature_list = self.get_feature_dict()

        ret_feature_list = []
        for idx, backup_data in enumerate(backup_data_list):
            ret_data = dict()
            current_feature_data = self.parse_features(backup_data)
            ret_data[Constants.backup_features_dict_name] = current_feature_data

            # Do stuff for next cycle
            action_data = {
                Constants.action_rename: current_feature_data['rename_amount'],
                Constants.action_deleted: current_feature_data['delete_amount'],
                Constants.action_added: current_feature_data['added_amount'],
                Constants.action_modified: current_feature_data['modified_amount'],
            }

            ret_data[Constants.action_data_dict_name] = action_data

            prev_file_tree = FileTreeDatabase(backup_data)
            self.file_database.add_backup_data(backup_data)
            if keep_prev_file_tree:
                ret_data[Constants.file_tree_dict_name] = prev_file_tree.get_storable_elements()

            if idx != len(backup_data_list) - 1:
                self.feature_extractors = self.create_feature_extractors(
                    prev_file_tree, action_data, self.file_database, self.path_separator
                )
                self.feature_list = self.get_feature_dict()

            ret_feature_list.append(ret_data)

        return ret_feature_list

    def parse_features(self, backup_data):
        """
        Given the backup data call all the feature extractors and receive their features
        :param backup_data:
        :return:
        """
        feature_dict = {}
        for feature_extractor in self.feature_extractors.values():
            feature_extractor.calc_features(backup_data)

        for feature, getter_function in self.feature_list.items():
            feature_dict[feature] = getter_function()

        return feature_dict

    def get_file_database(self):
        return self.file_database

    def get_file_database_as_string(self):
        return self.file_database.get_storable_elements()

    def general_feature_extractor(self):
        return self.feature_extractors['general_features']

    def action_feature_extractor(self):
        return self.feature_extractors['action_features']

    def date_feature_extractor(self):
        return self.feature_extractors['date_features']

    def path_feature_extractor(self):
        return self.feature_extractors['path_features']

    def user_feature_extractor(self):
        return self.feature_extractors['user_features']

    @staticmethod
    def create_feature_extractors(prev_file_tree, prev_action_data, file_database, path_separator):
        return dict(
            general_features = GeneralFeatures(prev_file_tree),
            action_features = ActionFeatures(prev_action_data),
            date_features = DateFeatures(),
            path_features = PathFeatures(prev_file_tree, file_database, path_separator = path_separator),
            user_features = UserFeatures(file_database)
        )

    def get_feature_dict(self) -> Dict[str, Callable]:
        ret_dict = dict()
        for feature_dict in list(map(lambda x: x.get_feature_list(), self.feature_extractors.values())):
            for key, callback in feature_dict.items():
                if key in ret_dict:
                    raise FeatureAlreadyDefined(f'The feature {key} was already defined. ')
                ret_dict[key] = callback

        return ret_dict
