from src.loader.database.dbmodels.IFileServerModel import IFileServerModel


class FileServerModel:
    def __init__(self,
                 use_path_features: bool = True,
                 use_meta_data_features: bool = True,
                 use_file_features: bool = False):

        self.meta_data_model = None
        self.path_ocsvm = None
        self.file_feature_model = None

    def fit(self):
        pass

    def predict(self):
        pass

    def load(self, loaded_model: IFileServerModel):
        pass

    def get_storable_components(self) -> IFileServerModel:
        return None