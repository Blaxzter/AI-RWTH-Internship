from dataclasses import dataclass
from typing import Dict

from bson import ObjectId


@dataclass
class IFileServerModel:
    """Mongo db file server model data model."""
    _id: ObjectId = None
    file_server: ObjectId = None
    path_ocsvm: Dict = None
    meta_data_model: Dict = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, v: ObjectId) -> None:
        self._id = v
