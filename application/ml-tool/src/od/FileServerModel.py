from typing import Optional, Dict

from bson import ObjectId

from src.Exceptions import NotInitializedException
from src.loader.database.dbmodels.IFileServerModel import IFileServerModel
from src.od.MetaDataModel import MetaDataModel
from src.od.PathOcsvm import PathOCSVM


class FileServerModel:
    def __init__(self,
                 file_server_id: ObjectId,
                 use_path_features: bool = True,
                 use_meta_data_features: bool = True,
                 use_file_features: bool = False,
                 file_path_separator = '/'):

        self.id = None
        self.file_server_id = file_server_id
        self.use_path_features = use_path_features
        self.use_meta_data_features = use_meta_data_features
        self.use_file_features = use_file_features

        self.file_path_separator = file_path_separator

        self.initialized = False
        self.meta_data_model: Optional[MetaDataModel] = MetaDataModel(self.file_path_separator)
        self.path_ocsvm: Optional[PathOCSVM] = PathOCSVM(self.file_path_separator)

    def initialize_model(self, stored_data: Optional[IFileServerModel] = None):
        if stored_data and stored_data.id:
            self.id = id

        if self.use_meta_data_features:
            if stored_data is not None and stored_data.meta_data_model is not None:
                self.meta_data_model.initialize_model(stored_data.meta_data_model)
            else:
                self.meta_data_model.initialize_model(None)

        if self.use_path_features:
            if stored_data is not None and stored_data.path_ocsvm is not None:
                self.path_ocsvm.initialize_model(stored_data.path_ocsvm)
            else:
                self.path_ocsvm.initialize_model(None)

        if self.use_file_features:
            raise NotImplementedError("Sorry file features are to expensive at the moment.")

        self.initialized = True

    def fit(self, backup_data_list):
        if self.initialized is False:
            raise NotInitializedException('Pls call initialize model before using the file server model.')

        collected_data = {}

        if self.use_meta_data_features:
            collected_data['meta_data_model'] = self.meta_data_model.fit(backup_data_list)

        if self.use_path_features:
            collected_data['path_ocsvm'] = self.path_ocsvm.fit(backup_data_list)

        return collected_data

    def predict(self, backup_data_collection, continues_training = True, ret_backup_features = True):

        backup_date = backup_data_collection['date']
        backup_data = backup_data_collection['backup_data']
        prev_backup_data = backup_data_collection['prev_backup_data']

        ret_dict = dict(
            backup_date = backup_date,
        )

        if self.use_meta_data_features:
            if ret_backup_features:
                desc_boundary, backup_metadata = self.meta_data_model.predict(
                    backup_data, prev_backup_data, add_to_model = continues_training, ret_backup_metadata = True
                )
                ret_dict['meta_data_model'] = dict(
                    prediction = desc_boundary,
                    backup_metadata = backup_metadata
                )
            else:
                desc_boundary = self.meta_data_model.predict(
                    backup_data, prev_backup_data, add_to_model = continues_training, ret_backup_metadata = False
                )
                ret_dict['meta_data_model'] = dict(
                    prediction = desc_boundary
                )

        return ret_dict

    def get_storable_components(self) -> IFileServerModel:
        return IFileServerModel(
            _id = self.id,
            file_server = self.file_server_id,
            path_ocsvm = self.path_ocsvm.get_stored_model() if self.path_ocsvm else None,
            meta_data_model = self.meta_data_model.get_stored_model() if self.meta_data_model else None,
        )
