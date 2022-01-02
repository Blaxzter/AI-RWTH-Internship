from dataclasses import dataclass

from typing import Dict

from bson import ObjectId


@dataclass
class IBackupMetaData:
    """Mongo db backup meta data, data model."""
    predictions: Dict
    features: Dict
    action_data: Dict

    backup_date: int
    # ID's
    file_server_id: ObjectId
    _id: ObjectId = None

    @property
    def id(self):
        return self._id
