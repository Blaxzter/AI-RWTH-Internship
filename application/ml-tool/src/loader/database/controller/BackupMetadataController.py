from pymongo.results import InsertOneResult


class BackupMetadataController:

    def __init__(self, db):
        self.db = db
        self.col = db.get_collection('col_backup_metadata')

    def get_backup_metadata_by_file_server_id(self, file_server_id):
        search_query = dict(file_server = file_server_id)
        return self.col.find(search_query)

    def get_backup_metadata_by_file_server_id_as_list(self, file_server_id):
        return list(self.get_backup_metadata_by_file_server_id(file_server_id))

    def add_backup_meta_data(self, file_server_id, meta_data) -> InsertOneResult:
        store_data = dict(meta_data)

        store_data['file_server'] = file_server_id
        return self.col.insert_one(store_data)
