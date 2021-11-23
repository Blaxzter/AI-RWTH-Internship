from dataclasses import dataclass

from bson import ObjectId


@dataclass
class FileServer:
    """Mongo db file server data model."""
    _id: ObjectId
    con: str
    check_schedule: int
    name: str

    # responsible_person: str

    @property
    def id(self):
        return self._id
