
class IFeatureExtractor:

    def __init__(self):
        self.features_calculated = False

    def get_feature_list(self) -> dict:
        pass

    def calc_features(self, backup_data):
        pass

    def reset(self):
        pass
