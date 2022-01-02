from dataclasses import asdict

from pymongo.results import InsertOneResult
from bson import ObjectId

from src.loader.database.dbmodels.IBackupMetaDataFiletree import IBackupMetaDataFileTree
from src.loader.database.dbmodels.IBackupMetaData import IBackupMetaData
from src.utils import Constants, Utils


class BackupMetadataController:

    def __init__(self, db):
        self.db = db
        self.col_backup_metadata = db.get_collection('col_backup_metadata')
        self.col_file_tree = db.get_collection('col_backup_metadata_filetree')

    def get_backup_metadata_by_file_server_id(self, file_server_id):
        search_query = dict(file_server_id = file_server_id)
        return self.col_backup_metadata.find(search_query)

    def get_backup_metadata_by_file_server_id_as_list(self, file_server_id):
        return list(self.get_backup_metadata_by_file_server_id(file_server_id))

    def get_last_backup_metadata_by_file_server_id(self, file_server_id):
        search_query = dict(file_server_id = file_server_id)
        sort_query = [('backup_date', -1)]
        found_meta_data = self.col_backup_metadata.find_one(search_query, sort = sort_query)
        if found_meta_data is not None:
            file_tree_search_query = dict(backup_metadata_id = found_meta_data['_id'])
            file_tree_data = self.col_file_tree.find_one(file_tree_search_query)
            found_meta_data[Constants.file_tree_dict_name] = file_tree_data['filetree']

        return found_meta_data

    def add_backup_meta_data(self, file_server_id: ObjectId, meta_data) -> InsertOneResult:
        data = meta_data[Constants.backup_metadata_dict_name]
        store_data = IBackupMetaData(
            backup_date = meta_data[Constants.backup_date_dict_name],
            predictions = meta_data[Constants.prediction_dict_name] if Constants.prediction_dict_name in meta_data else None,
            features = data[Constants.backup_features_dict_name],
            action_data = data[Constants.action_data_dict_name],
            file_server_id = file_server_id
        )
        insert_query = asdict(store_data, dict_factory = Utils.dict_factory)
        return self.col_backup_metadata.insert_one(insert_query)

    def add_backup_meta_data_file_tree(self, backup_metadata_id: ObjectId, file_tree_data):
        store_data = IBackupMetaDataFileTree(backup_metadata_id = backup_metadata_id, filetree = file_tree_data)
        insert_query = asdict(store_data, dict_factory = Utils.dict_factory)
        return self.col_file_tree.insert_one(insert_query)
