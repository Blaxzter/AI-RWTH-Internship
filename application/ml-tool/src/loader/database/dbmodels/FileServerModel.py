from dataclasses import dataclass
from typing import Dict

from bson import ObjectId


@dataclass
class FileServerModel:
    """Mongo db file server model data model."""
    svm: Dict
    file_server: ObjectId
    _id: ObjectId = None
    od_model: str = None

    @property
    def id(self):
        return self._id
