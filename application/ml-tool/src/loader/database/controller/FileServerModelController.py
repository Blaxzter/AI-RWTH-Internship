from dataclasses import asdict
from typing import Optional

from src.Exceptions import ODModelExists
from src.loader.database.dbmodels.IFileServerModel import IFileServerModel
from src.utils.Utils import dict_factory


class FileServerModelController:

    def __init__(self, db):
        self.db = db
        self.col = db.col_file_server_model

    def get_file_server_model(self, file_server_id) -> Optional[IFileServerModel]:
        search_query = dict(file_server = file_server_id)
        found_file_server_model = self.col.find_one(search_query)

        if found_file_server_model is None:
            return None

        return IFileServerModel(**found_file_server_model)

    def add_file_server_model(self, file_server_model: IFileServerModel):
        # Check if file server exists
        if file_server_model.id is not None and self.col.count_documents(
                dict(file_server_id = file_server_model.id)) != 0:
            raise ODModelExists(f"file sever with id {file_server_model.id} already got a model.")

        insert_query = asdict(file_server_model, dict_factory = dict_factory)
        return self.col.insert_one(insert_query)

    def update_file_server_model(self, file_server_model: IFileServerModel):
        search_query = dict(file_server_id = file_server_model.id)
        update_query = {'$set': asdict(file_server_model, dict_factory = dict_factory)}

        return self.col.update_one(search_query, update_query)


