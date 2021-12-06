from typing import Optional

from src.loader.database.dbmodels.IFileServer import IFileServer


class FileServerController:

    def __init__(self, db):
        self.db = db
        self.col = db.col_file_server

    def get_file_server_by_name(self, name) -> Optional[IFileServer]:
        found_file_server = self.col.find_one(dict(name = name))
        if found_file_server is None:
            return None

        return IFileServer(**found_file_server)

    def add_file_server(self, name, con, check_schedule):
        # Check if file server exists
        if self.col.count_documents(dict(name = name)) != 0:
            raise Warning(f"file sever {name} already exists")

        return self.col.insert_one(dict(
            con = con,
            check_schedule = check_schedule,
            name = name,
        ))

