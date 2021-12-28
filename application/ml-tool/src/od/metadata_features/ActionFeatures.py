import numpy as np

from src.Exceptions import FeatureNotCalculated
from src.od.metadata_features.IFeatureExtractor import IFeatureExtractor
from src.utils import Constants


class ActionFeatures(IFeatureExtractor):
    def __init__(self, prev_backup_actions = None):

        super().__init__()
        self.prev_backup_actions = prev_backup_actions

        self.rename_amount = 0
        self.deleted_amount = 0
        self.modified_amount = 0
        self.added_amount = 0

        self.rename_delta = 0
        self.deleted_delta = 0
        self.modified_delta = 0
        self.added_delta = 0

    def get_feature_list(self):
        return dict(
            # Action feature
            rename_amount = self.get_rename_amount_feature,
            rename_delta = self.get_rename_delta_feature,
            delete_amount = self.get_deleted_amount_feature,
            delete_delta = self.get_deleted_delta_feature,
            added_amount = self.get_added_amount_feature,
            added_delta = self.get_added_delta_feature,
            modified_amount = self.get_modified_amount_feature,
            modified_delta = self.get_modified_delta_feature,
        )

    def calc_features(self, backup_data):
        # Get the paths from the feature list
        action_list = list(map(lambda feature: feature[Constants.action_index], backup_data))

        uniques, counts = np.unique(action_list, return_counts = True)
        self.rename_amount = self.get_unique_count_or_zero(uniques, counts, Constants.action_rename)
        self.deleted_amount = self.get_unique_count_or_zero(uniques, counts, Constants.action_deleted)
        self.modified_amount = self.get_unique_count_or_zero(uniques, counts, Constants.action_modified)
        self.added_amount = self.get_unique_count_or_zero(uniques, counts, Constants.action_added)

        if self.prev_backup_actions is not None:
            self.rename_delta = self.prev_backup_actions[Constants.action_rename] - self.rename_amount
            self.deleted_delta = self.prev_backup_actions[Constants.action_deleted] - self.deleted_amount
            self.modified_delta = self.prev_backup_actions[Constants.action_modified] - self.modified_amount
            self.added_delta = self.prev_backup_actions[Constants.action_added] - self.added_amount

        self.features_calculated = True

    @staticmethod
    def get_unique_count_or_zero(uniques, counts, unique):
        unique_idx = np.where(uniques == unique)
        value = counts[unique_idx]
        if len(value) > 0:
            return value.item()
        else:
            return 0

    def get_rename_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The rename_amount_feature is not calculated. Pls. call calc_features first')
        return self.rename_amount

    def get_deleted_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The deleted_amount_feature is not calculated. Pls. call calc_features first')
        return self.deleted_amount

    def get_modified_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The modified_amount_feature is not calculated. Pls. call calc_features first')
        return self.modified_amount

    def get_added_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The added_amount_feature is not calculated. Pls. call calc_features first')
        return self.added_amount

    def get_rename_delta_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The rename_delta_feature is not calculated. Pls. call calc_features first')
        return self.rename_delta

    def get_deleted_delta_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The deleted_delta_feature is not calculated. Pls. call calc_features first')
        return self.deleted_delta

    def get_modified_delta_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The modified_delta_feature is not calculated. Pls. call calc_features first')
        return self.modified_delta

    def get_added_delta_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The added_delta_feature is not calculated. Pls. call calc_features first')
        return self.added_delta
