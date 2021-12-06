from dataclasses import dataclass

from typing import Dict, List

from bson import ObjectId


@dataclass
class IBackupMetaData:
    """Mongo db backup meta data, data model."""
    _id: ObjectId
    backed_up_amount: int
    uniques_counts: Dict
    date_range: Dict
    date_mean_std: Dict
    file_server: ObjectId

    @property
    def id(self):
        return self._id
