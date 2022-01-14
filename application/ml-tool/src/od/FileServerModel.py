from typing import Optional, Dict, List

from bson import ObjectId

from src.Exceptions import NotInitializedException, PreviousBackupRequired
from src.loader.database.dbmodels.IFileServerModel import IFileServerModel
from src.od.MetaDataModel import MetaDataModel
from src.od.PathOcsvm import PathOCSVM
from src.utils import Constants


class FileServerModel:
    def __init__(self,
                 file_server_id: ObjectId,
                 model_id: Optional[ObjectId] = None,
                 use_path_features: bool = True,
                 use_meta_data_features: bool = True,
                 use_file_features: bool = False,
                 file_path_separator = '/'):

        self.model_id = None
        self.file_server_id = file_server_id
        self.use_path_features = use_path_features
        self.use_meta_data_features = use_meta_data_features
        self.use_file_features = use_file_features

        self.file_path_separator = file_path_separator

        self.initialized = False
        self.meta_data_model: Optional[MetaDataModel] = MetaDataModel(self.file_path_separator)
        self.path_ocsvm: Optional[PathOCSVM] = PathOCSVM(self.file_path_separator)

    def get_used_models(self):
        ret_list = []
        if self.use_path_features:
            ret_list.append('path_ocsvm')
        if self.use_meta_data_features:
            ret_list.append('meta_data_model')
        if self.use_file_features:
            ret_list.append('file_feature_model')
        return ret_list

    def initialize_model(self, stored_data: Optional[IFileServerModel] = None, prev_backup_data = None):

        if self.use_meta_data_features:
            if stored_data is not None and stored_data.meta_data_model is not None:
                # Merge the data from the prev backup with the stored data for the metadata model
                for key, value in prev_backup_data.items():
                    stored_data.meta_data_model[key] = value
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

    def fit(self, backup_data_collection: List) -> Dict:
        if self.initialized is False:
            raise NotInitializedException('Pls call initialize model before using the file server model.')

        backup_data_list = list(map(lambda x: x['backup_data'], backup_data_collection))
        backup_data_dates = list((map(lambda x: x['backup_date'], backup_data_collection)))
        collected_data = dict()

        if self.use_meta_data_features:
            fitted_meta_data_model = self.meta_data_model.fit(backup_data_list)
            collected_data['meta_data_model'] = list(map(
                lambda z_object: dict(
                    backup_date = z_object[0],
                    backup_metadata = z_object[1],
                ), zip(backup_data_dates, fitted_meta_data_model)))

        if self.use_path_features:
            self.path_ocsvm.fit(backup_data_list)

        return collected_data

    def predict(self, backup_data_collection, prev_backup_data = None, continues_training = True,
                ret_backup_features = True):

        # These two as lists
        backup_data_list = list(map(lambda x: x['backup_data'], backup_data_collection))
        backup_data_dates = list((map(lambda x: x['backup_date'], backup_data_collection)))

        ret_dict = dict()

        if self.use_meta_data_features:

            if prev_backup_data is None:
                raise PreviousBackupRequired("In order to use the Meta data model, the previous backup is required.")

            if Constants.verbose_printing:
                print('Predict Meta Data Model')

            if ret_backup_features:
                prediction, confidence, desc_boundary, backup_metadata = self.meta_data_model.predict(
                    backup_data_list, prev_backup_data, add_to_model = continues_training, ret_backup_metadata = True
                )

                # Merge results of the model with the list of dates into a returnable data structure
                data_list = []
                for idx, backup_date in enumerate(backup_data_dates):
                    data_list.append({
                        Constants.backup_date_dict_name: backup_date,
                        Constants.dist_to_disc_dict_name: desc_boundary[idx],
                        Constants.pred_confidence_dict_name: confidence[idx],
                        Constants.prediction_dict_name: prediction[idx],
                        Constants.backup_metadata_dict_name: backup_metadata[idx]
                    })
                ret_dict['meta_data_model'] = data_list

            else:
                prediction, confidence, desc_boundary = self.meta_data_model.predict(
                    backup_data_list, prev_backup_data, add_to_model = continues_training, ret_backup_metadata = False
                )
                ret_dict['meta_data_model'] = [{
                    Constants.backup_date_dict_name: backup_date,
                    Constants.dist_to_disc_dict_name: desc_boundary,
                    Constants.pred_confidence_dict_name: confidence,
                    Constants.prediction_dict_name: prediction,
                } for backup_date, prediction, confidence, desc_boundary in
                    zip(backup_data_dates, prediction, confidence, desc_boundary)]

        if self.use_path_features:
            if Constants.verbose_printing:
                print('Predict path ocsvm model')
            prediction, confidence, desc_boundary = self.path_ocsvm.predict(
                backup_data_list, continues_training = continues_training
            )
            ret_dict['path_ocsvm'] = [{
                Constants.backup_date_dict_name: backup_date,
                Constants.dist_to_disc_dict_name: desc_boundary,
                Constants.pred_confidence_dict_name: confidence,
                Constants.prediction_dict_name: prediction,
            } for backup_date, prediction, confidence, desc_boundary in
                zip(backup_data_dates, prediction, confidence, desc_boundary)]

        return ret_dict

    def re_predict(self):

        ret_dict = dict()

        if self.use_meta_data_features:
            ret_dict['meta_data_model'] = self.meta_data_model.re_predict()

        if self.use_path_features:
            ret_dict['path_ocsvm'] = self.path_ocsvm.re_predict()

        return ret_dict

    def get_storable_components(self) -> IFileServerModel:

        meta_data_model = None
        if self.meta_data_model and self.meta_data_model.initialized:
            meta_data_model = self.meta_data_model.get_stored_model()

        path_ocsvm = None
        if self.path_ocsvm and self.path_ocsvm.initialized:
            path_ocsvm = self.path_ocsvm.get_stored_model()

        return IFileServerModel(
            _id = self.model_id,
            file_server = self.file_server_id,
            path_ocsvm = path_ocsvm,
            meta_data_model = meta_data_model,
        )
