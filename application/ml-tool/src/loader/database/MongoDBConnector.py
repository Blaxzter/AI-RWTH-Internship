import pymongo

from src.loader.database.controller.BackupMetadataController import BackupMetadataController
from src.loader.database.controller.FileDataController import FileDataController
from src.loader.database.controller.FileServerController import FileServerController
from src.loader.database.controller.FileServerModelController import FileServerModelController


class MongoDBConnector(FileServerController, BackupMetadataController, FileServerModelController, FileDataController):

    def __init__(self):
        self.con = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_mltool = self.con["mltool"]

        self.collections = dict(
            col_file_server = self.db_mltool["file_server"],
            col_file_server_model = self.db_mltool["file_server_model"],
            col_backup_metadata = self.db_mltool["backup_metadata"],
            col_file_feature_history = self.db_mltool["file_feature_history"],
            col_file_features = self.db_mltool["file_features"],
        )
        super().__init__(db = self)

    def get_collection(self, name: str):
        return self.collections[name]

    def reset_data(self):
        for collection in self.collections.values():
            collection.drop()


def create_example_server(db_con):
    example_server_data = dict(
        con = "example connection",
        check_schedule = 2,
        name = 'test_file_server'
    )

    file_server = db_con.get_file_server_by_name('test_file_server')

    if file_server is None:
        file_server_res = db_con.add_file_server(
            name = example_server_data['name'],
            con = example_server_data['con'],
            check_schedule = example_server_data['check_schedule'],
        )
        if file_server_res.acknowledged:
            file_server = dict(example_server_data)
            file_server['_id'] = file_server_res.inserted_id
        else:
            raise Exception('Some thing went wrong with the file server creation')

    return file_server


if __name__ == '__main__':
    mongoDBCon = MongoDBConnector()
    file_server = create_example_server(mongoDBCon)
    print(file_server)
    created_data = mongoDBCon.add_backup_meta_data(
        file_server['_id'],
        {
            'backed_up_amount': 578,
            'uniques_counts': (['A', 'D', 'M'], [521, 14, 43]),
            'date_range': (1537260310.0, 1537948386.0),
            'date_mean_std': (0.07818695784208826, 0.23521734927004326)
        }
    )
    print(mongoDBCon.db_mltool.list_collection_names())
