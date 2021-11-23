from dataclasses import asdict
from typing import Optional

import pymongo
from pymongo.results import InsertOneResult

from src.Exceptions import ODModelExists
from src.loader.database.dbmodels.FileServer import FileServer
from src.loader.database.dbmodels.FileServerModel import FileServerModel
from src.utils.Utils import dict_factory


class MongoDBConnector:

    def __init__(self):
        self.con = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_mltool = self.con["mltool"]

        self.col_file_server = self.db_mltool["file_server"]
        self.col_file_server_model = self.db_mltool["file_server_model"]
        self.col_backup_metadata = self.db_mltool["backup_metadata"]
        self.col_file_feature_history = self.db_mltool["file_feature_history"]
        self.col_file_features = self.db_mltool["file_features"]

        self.collections = [
            self.col_file_features,
            self.col_file_server,
            self.col_file_server_model,
            self.col_backup_metadata,
            self.col_file_feature_history
        ]

    def get_file_server_model(self, file_server_id) -> Optional[FileServerModel]:
        search_query = dict(file_server = file_server_id)
        found_file_server_model = self.col_file_server_model.find_one(search_query)
        if found_file_server_model is None:
            return None

        return FileServerModel(**found_file_server_model)

    def add_file_server_model(self, fileServerModel: FileServerModel):
        # Check if file server exists
        if fileServerModel.id is not None and self.col_file_server.count_documents(
                dict(file_server_id = fileServerModel.id)) != 0:
            raise ODModelExists(f"file sever with id {fileServerModel.id} already got a model.")

        insert_query = asdict(fileServerModel, dict_factory = dict_factory)
        return self.col_file_server_model.insert_one(insert_query)

    def update_file_server_model(self, fileServerModel: FileServerModel):
        search_query = dict(file_server_id = fileServerModel.id)
        update_query = {'$set': asdict(fileServerModel, dict_factory = dict_factory)}

        return self.col_file_server_model.update_one(search_query, update_query)

    def get_file_server_by_name(self, name) -> FileServer:
        found_file_server = self.col_file_server.find_one(dict(name = name))
        return FileServer(**found_file_server)

    def add_file_server(self, name, con, check_schedule):
        # Check if file server exists
        if self.col_file_server.count_documents(dict(name = name)) != 0:
            raise Warning(f"file sever {name} already exists")

        return self.col_file_server.insert_one(dict(
            con = con,
            check_schedule = check_schedule,
            name = name,
        ))

    def get_file_data(self, file_server_id):
        search_query = dict(file_server = file_server_id)
        return self.col_file_feature_history.find(search_query)

    def get_file_data_as_list(self, file_server_id):
        return list(self.get_file_data(file_server_id))

    def add_file_data(self, file_server_id, backup_data_id, file_data_list):
        for file_data in file_data_list:
            file_data['file_server'] = file_server_id
            file_data['backup_data'] = backup_data_id
            self.col_file_features.update_one(
                dict(file_server = file_server_id,
                     name = file_data['name']),
                {'$set': file_data},
                upsert = True
            )
        return self.col_file_feature_history.insert(file_data_list)

    def add_backup_meta_data(self, file_server_id, meta_data) -> InsertOneResult:
        store_data = dict(meta_data)

        store_data['file_server'] = file_server_id
        return self.col_backup_metadata.insert_one(store_data)

    def reset_data(self):
        for collection in self.collections:
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
