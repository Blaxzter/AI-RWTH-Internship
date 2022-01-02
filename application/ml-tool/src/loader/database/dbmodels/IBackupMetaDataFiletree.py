from dataclasses import dataclass

from typing import Dict, List, Optional

from bson import ObjectId


@dataclass
class IBackupMetaDataFileTree:
    """Mongo db backup meta data file tree, data model."""
    filetree: str

    # Required ID
    backup_metadata_id: ObjectId
    _id: Optional[ObjectId] = None

    @property
    def id(self):
        return self._id
