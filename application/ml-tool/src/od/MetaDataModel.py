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

from src.Exceptions import NotInitializedException
from src.od.metadata_features.ActionFeatures import ActionFeatures
from src.od.metadata_features.DateFeatures import DateFeatures
from src.od.metadata_features.GeneralFeatures import GeneralFeatures
from src.od.metadata_features.PathFeatures import PathFeatures
from src.od.metadata_features.UserFeatures import UserFeatures
from src.od.searchutils.FileTreeDatabase import FileTreeDatabase
from src.utils import Constants


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

        self.trained_features = []
        self.clf = None

    def initialize_model(self, stored_data: Optional[Dict] = None):
        if stored_data:
            self.clf = pickle.loads(stored_data['model'])
            self.trained_features = stored_data['trained_features']
            self.prev_action_data = stored_data['action_data']

            prev_file_tree_json = stored_data['file_tree']
            self.prev_file_tree = FileTreeDatabase(path_separator = self.path_separator)
            self.prev_file_tree.load_from_string(prev_file_tree_json)

            file_database_json = stored_data['file_database']
            self.file_database = FileTreeDatabase(path_separator = self.path_separator, add_user = True)
            self.file_database.load_from_string(file_database_json)

            self.feature_extractors = self.create_feature_extractors(
                self.prev_file_tree, self.prev_action_data, self.file_database, self.path_separator
            )
            self.feature_list = self.get_feature_dict()
            self.feature_scalers = pickle.loads(stored_data['feature_scalers'])
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
            self.clf = SUOD(base_estimators = detector_list, n_jobs = 1, combination = 'average', verbose = False)

        self.feature_amount = len(self.feature_list)
        self.initialized = True

    def fit(self, backup_data_list):
        if not self.initialized:
            raise NotInitializedException('The meta data model is not initialized')

        backup_features = self.parse_features_of_list(backup_data_list)
        self.trained_features = backup_features
        train_matrix = self.vectorise(meta_data_feature_list = backup_features, train = True)
        self.clf.fit(train_matrix)

    def predict(self, backup_data, add_to_model = False, ret_backup_features = True):
        if not self.initialized:
            raise NotInitializedException('The meta data model is not initialized')

        backup_features = self.parse_features(backup_data)
        test_matrix = self.vectorise([backup_features], train = False)
        desc_boundary = self.clf.decision_function(test_matrix)

        if add_to_model:
            # Add the new backup data to the trained model
            self.trained_features.append(backup_features)
            if self.truncate_train_data > 0:
                # Todo throw away oldest stored stuff
                pass
            train_matrix = self.vectorise(meta_data_feature_list = self.trained_features, train = True)
            self.clf.fit(train_matrix)

            self.file_database.add_backup_data(backup_data)

        if ret_backup_features:
            return desc_boundary, backup_features
        else:
            return desc_boundary

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

    def parse_features_of_list(self, backup_data_list):

        self.file_database = FileTreeDatabase(path_separator = self.path_separator, add_user = True)

        self.feature_extractors = self.create_feature_extractors(None, None, self.file_database, self.path_separator)
        self.feature_list = self.get_feature_dict()

        ret_feature_list = []
        for backup_data in backup_data_list:
            current_feature_data = self.parse_features(backup_data)
            ret_feature_list.append(current_feature_data)

            # Do stuff for next cycle
            prev_action_data = {
                Constants.action_rename: current_feature_data['rename_amount'],
                Constants.action_deleted: current_feature_data['delete_amount'],
                Constants.action_added: current_feature_data['added_amount'],
                Constants.action_modified: current_feature_data['modified_amount'],
            }

            prev_file_tree = FileTreeDatabase(backup_data)
            self.file_database.add_backup_data(backup_data)

            self.feature_extractors = self.create_feature_extractors(
                prev_file_tree, prev_action_data, self.file_database, self.path_separator
            )
            self.feature_list = self.get_feature_dict()

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
        return dict(
            # General features
            amount = self.general_feature_extractor().get_amount_feature,
            amount_delta = self.general_feature_extractor().get_delta_amount_feature,

            # Action feature
            rename_amount = self.action_feature_extractor().get_rename_amount_feature,
            rename_delta = self.action_feature_extractor().get_rename_delta_feature,
            delete_amount = self.action_feature_extractor().get_deleted_amount_feature,
            delete_delta = self.action_feature_extractor().get_deleted_delta_feature,
            added_amount = self.action_feature_extractor().get_added_amount_feature,
            added_delta = self.action_feature_extractor().get_added_delta_feature,
            modified_amount = self.action_feature_extractor().get_modified_amount_feature,
            modified_delta = self.action_feature_extractor().get_modified_delta_feature,

            # Date Feature (Subtracted date day from days)
            start_time = self.date_feature_extractor().get_start_time_feature,
            end_time = self.date_feature_extractor().get_end_time_feature,
            time_range = self.date_feature_extractor().get_time_range_feature,
            time_standard_deviation = self.date_feature_extractor().get_time_standard_deviation_feature,
            time_avg = self.date_feature_extractor().get_time_avg_feature,

            # Path features
            min_path_length = self.path_feature_extractor().get_min_path_length_feature,
            max_path_length = self.path_feature_extractor().get_max_path_length_feature,
            avg_path_length = self.path_feature_extractor().get_avg_path_length_feature,
            min_branching_factor = self.path_feature_extractor().get_min_branching_factor_feature,
            max_branching_factor = self.path_feature_extractor().get_max_branching_factor_feature,
            avg_branching_factor = self.path_feature_extractor().get_avg_branching_factor_feature,

            # Folder / Files
            diff_folders_amount = self.path_feature_extractor().get_diff_folders_amount_feature,
            amount_type_endings = self.path_feature_extractor().get_amount_type_endings_feature,
            avg_file_ending_amounts = self.path_feature_extractor().get_avg_file_ending_amounts_feature,
            amount_not_previously_stored = self.path_feature_extractor().get_amount_not_previously_stored_feature,
            cross_section = self.path_feature_extractor().get_cross_section_feature,

            # User
            amount_users = self.user_feature_extractor().get_amount_users_feature,
            changed_user = self.user_feature_extractor().get_changed_user_feature,
            avg_file_per_user = self.user_feature_extractor().get_avg_file_per_user_feature,
            min_file_per_user = self.user_feature_extractor().get_min_file_per_user_feature,
            max_file_per_user = self.user_feature_extractor().get_max_file_per_user_feature,
        )
