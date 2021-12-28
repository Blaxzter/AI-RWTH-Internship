from src.Exceptions import FeatureNotCalculated
from src.od.metadata_features.IFeatureExtractor import IFeatureExtractor
from src.od.searchutils.FileTreeDatabase import FileTreeDatabase


class GeneralFeatures(IFeatureExtractor):
    def __init__(self, prev_backup: FileTreeDatabase):

        super().__init__()
        self.prev_backup = prev_backup

        self.amount = 0
        self.delta_amount = 0

    def calc_features(self, backup_data):
        self.amount = len(backup_data)

        if self.prev_backup is not None:
            self.delta_amount = self.prev_backup.size - self.amount
        else:
            self.delta_amount = 0

        self.features_calculated = True

    def get_feature_list(self):
        return dict(
            # General features
            amount = self.get_amount_feature,
            amount_delta = self.get_delta_amount_feature,
        )

    def get_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The amount feature is not calculated. Pls. call calc_features first')
        return self.amount

    def get_delta_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The delta amount feature is not calculated. Pls. call calc_features first')
        return self.delta_amount
