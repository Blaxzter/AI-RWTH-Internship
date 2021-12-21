import numpy as np

from src.Exceptions import FeatureNotCalculated
from src.od.searchutils.FileTreeDatabase import FileTreeDatabase
from src.utils import Constants


class UserFeatures:
    def __init__(self, data_base: FileTreeDatabase = None,):

        self.data_base = data_base

        self.amount_users = 0
        self.changed_user = 0
        self.min_file_per_user = 0
        self.max_file_per_user = 0
        self.avg_file_per_user = 0

        self.features_calculated = False

    def calc_features(self, backup_data):
        users = list(map(lambda file_data: file_data[Constants.user_index], backup_data))

        uniques, counts = np.unique(users, return_counts = True)

        self.amount_users = len(uniques)
        self.min_file_per_user = counts.min()
        self.max_file_per_user = counts.max()
        self.avg_file_per_user = np.average(counts)

        if self.data_base is not None and self.data_base.size != 0:
            for file_data in backup_data:
                file_node = self.data_base[file_data[Constants.name_index]]
                if file_node is not None:
                    self.changed_user += 1 if file_node.user != file_data[Constants.user_index] else 0

        self.features_calculated = True

    def get_amount_users_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The amount users feature is not calculated. Pls. call calc_features first')
        return self.amount_users

    def get_changed_user_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The changed users feature is not calculated. Pls. call calc_features first')
        return self.changed_user

    def get_min_file_per_user_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The min file per users feature is not calculated. Pls. call calc_features first')
        return self.min_file_per_user

    def get_max_file_per_user_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The max file per user feature is not calculated. Pls. call calc_features first')
        return self.max_file_per_user

    def get_avg_file_per_user_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The avg file per user feature is not calculated. Pls. call calc_features first')
        return self.avg_file_per_user
