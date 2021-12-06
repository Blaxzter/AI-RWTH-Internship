import time
from typing import Dict, List

import numpy as np
from dateutil.parser import parse
from pyod.models.copod import COPOD
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.suod import SUOD
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

from src.utils.Constants import action_index, date_index


class MetaDataModel:

    def __init__(self, train_data = None):
        self.train_data = train_data
        self.unix_date_scaler = preprocessing.MinMaxScaler()

        self.feature_list = [
            # General features
            'amount', 'amount_delta',

            # Action feature
            'rename_amount', 'rename_delta', 'delete_amount', 'delete_delta',
            'added_amount', 'added_delta', 'modified_amount', 'modified_delta',

            # Date Feature (Subtracted date day from days)
            'start_time', 'end_time', 'time_range'
            'time_std', 'time_avg',

            # Path features
            'min_path_length', 'max_path_length', 'avg_path_length',
            'min_branching_factor', 'max_branching_factor', 'avg_branching_factor',

            # Folder / Files
            'diff_folders', 'avg_dist', 'amount_file_endings',
            'previously_stored', 'cross_section',
            
            # User
            'Amount Users', 'changed_user',
            'avg_file_per_user', 'min_file_per_user', 'max_file_per_user',
        ]

        self.feature_amount = 10
        self.feature_scalers = {feature_name: StandardScaler() for feature_name in self.feature_list}

        # initialized a group of outlier detectors for acceleration
        detector_list = [LOF(n_neighbors = 15), LOF(n_neighbors = 20),
                         HBOS(n_bins = 10), HBOS(n_bins = 20),
                         COPOD(), IForest(n_estimators = 50),
                         IForest(n_estimators = 100),
                         IForest(n_estimators = 150)]
        # https://www.andrew.cmu.edu/user/yuezhao2/papers/21-mlsys-suod.pdf
        self.clf = SUOD(base_estimators = detector_list, n_jobs = 2, combination = 'average', verbose = False)

    def fit(self):
        backup_features = self.parse_features(self.train_data)
        train_matrix = self.vectorise(meta_data_feature_list = backup_features, train = True)
        self.clf.fit(train_matrix)

    def predict(self, backup_data_set):
        backup_features = self.parse_features(backup_data_set)
        test_matrix = self.vectorise(meta_data_feature_list = backup_features, train = False)
        return self.clf.decision_function(test_matrix)

    def flatten_feature_dict(self, feature_dict_list):
        for feature_dict in feature_dict_list:
            # todo put all the features next to one another
            pass

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
                    scaled_feature = feature_scaler.transform(feature)
                    data_array.append(scaled_feature)

            data_matrix[idx] = np.asarray(data_array)

        if train:
            # Go over each feature type and use a different scaler to scale independently
            for idx, scaler in enumerate(self.feature_scalers):
                feature_data = data_matrix[:, idx]
                scaler.fit(feature_data)
                data_matrix[:, idx] = scaler.transform(feature_data)

        return data_matrix

    def parse_features(self, backup_data_set):
        feature_list = []
        for backup_data in backup_data_set:
            backed_up_amount = len(backup_data)

            # Get the actions and counts of each action
            action_list = list(map(lambda d: d[action_index], backup_data))
            uniques, counts = np.unique(action_list, return_counts = True)

            # Todo Think about scaling of each feature group

            # Features of the backup dates

            # Get the mean and std deviation of the min max scaled date range of all changes
            parse_access_dates = list(map(lambda d: parse(d[date_index]), backup_data))
            unix_dates = np.array(list(map(lambda date: time.mktime(date.timetuple()), parse_access_dates)))
            unix_dates = unix_dates.reshape(-1, 1)
            unix_dates_scaled = self.unix_date_scaler.fit_transform(unix_dates)

            unix_dates_mean = np.mean(unix_dates_scaled)
            unix_dates_std = np.std(unix_dates_scaled)

            # Get the date ranges in unix time stamps
            sorted_access_dates = sorted(unix_dates)
            earliest_date = sorted_access_dates[0]
            latest_date = sorted_access_dates[-1]

            # distance from start of day, end of day, range,

            feature_list.append(dict(
                backed_up_amount = backed_up_amount,
                uniques_counts = dict(uniques = uniques.tolist(), counts = counts.tolist()),
                date_range = dict(earliest_date = earliest_date.item(), latest_date = latest_date.item()),
                date_mean_std = dict(unix_dates_mean = unix_dates_mean, unix_dates_std = unix_dates_std)
            ))

        return feature_list
