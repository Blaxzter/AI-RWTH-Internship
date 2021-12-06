
class FileDataController:

    def __init__(self, db):
        self.db = db
        self.col = db.get_collection('col_file_features')
        self.col_history = db.get_collection('col_file_feature_history')

    def get_file_data(self, file_server_id):
        search_query = dict(file_server = file_server_id)
        return self.col_history.find(search_query)

    def get_file_data_as_list(self, file_server_id):
        return list(self.get_file_data(file_server_id))

    def add_file_data(self, file_server_id, backup_data_id, file_data_list):
        for file_data in file_data_list:
            file_data['file_server'] = file_server_id
            file_data['backup_data'] = backup_data_id
            self.col.update_one(
                dict(file_server = file_server_id,
                     name = file_data['name']),
                {'$set': file_data},
                upsert = True
            )
        return self.col_history.insert(file_data_list)