from typing import Optional, Dict

from src.Exceptions import NotInitializedException
from src.loader.database.dbmodels.IFileServerModel import IFileServerModel
from src.od.MetaDataModel import MetaDataModel


class FileServerModel:
    def __init__(self,
                 use_path_features: bool = True,
                 use_meta_data_features: bool = True,
                 use_file_features: bool = False,
                 file_path_separator = '/'):

        self.use_path_features = use_path_features
        self.use_meta_data_features = use_meta_data_features
        self.use_file_features = use_file_features
        self.file_path_separator = file_path_separator

        self.initialized = False
        self.meta_data_model = MetaDataModel(self.file_path_separator)
        self.path_ocsvm = None

    def initialize_model(self, stored_data: Optional[IFileServerModel] = None):
        if self.use_meta_data_features:
            if stored_data is not None and stored_data.meta_data_model is not None:
                self.meta_data_model.initialize_model(stored_data.meta_data_model)
            else:
                self.meta_data_model.initialize_model(None)

        if self.use_path_features:
            self.path_ocsvm = None

        if self.use_file_features:
            raise NotImplementedError("Sorry file features are to expensive at the moment.")

        self.initialized = True

    def fit(self, backup_data_list):
        if self.initialized is False:
            raise NotInitializedException('Pls call initialize model before using the file server model.')

        self.meta_data_model.fit(backup_data_list)

    def predict(self, backup_data, continues_training = True, ret_backup_features = True):

        desc_boundary, backup_features = self.meta_data_model.predict(
            backup_data, add_to_model = continues_training, ret_backup_features = ret_backup_features
        )

        return dict(
            meta_data_prediction = desc_boundary,
            backup_features = backup_features
        )

    def get_storable_components(self) -> IFileServerModel:
        return None
