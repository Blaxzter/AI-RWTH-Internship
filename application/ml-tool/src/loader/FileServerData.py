from src.Exceptions import FileServerDoesntExists
from src.loader.FileDatabase import FileDatabase
from src.loader.database.MongoDBConnector import MongoDBConnector


class FileServerData:

    def __init__(self, db: MongoDBConnector, test_file_server_name: str, use_file_features: bool = False):
        self.db = db
        self.file_server_id = test_file_server_name
        self.use_file_features = use_file_features

        self.file_server = db.get_file_server_by_name(test_file_server_name)
        if self.file_server is None:
            raise FileServerDoesntExists('The requested file server doesn\'t exist')

        self.backup_metadata = db.get_backup_metadata_by_file_server_id_as_list(self.file_server.id)

        if use_file_features:
            file_feature_list = db.get_file_data_as_list(self.file_server.id)
            self.file_database = FileDatabase(file_feature_list, is_sorted = True)

    def get_backup_metadata(self):
        return self.backup_metadata

    def get_file_database(self):
        return self.backup_metadata
