from typing import Optional

from src.loader.database.dbmodels.IFileServer import IFileServer


class FileServerController:

    def __init__(self, db):
        self.db = db
        self.col_file_server = db.collections['col_file_server']

    def get_file_server_by_name(self, name) -> Optional[IFileServer]:
        found_file_server = self.col_file_server.find_one(dict(name = name))
        if found_file_server is None:
            return None

        return IFileServer(**found_file_server)

    def add_file_server(self, name, con, check_schedule):
        # Check if file server exists
        if self.col_file_server.count_documents(dict(name = name)) != 0:
            raise Warning(f"file sever {name} already exists")

        return self.col_file_server.insert_one(dict(
            con = con,
            check_schedule = check_schedule,
            name = name,
        ))

