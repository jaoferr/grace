from datetime import datetime

from beanie import Document, Indexed
from beanie.odm.fields import PydanticObjectId
from pymongo.operations import IndexModel
from pymongo import DESCENDING


class Tag(Document):
    name: Indexed(str)
    description: str
    timestamp_added: datetime = datetime.utcnow()
    user_id: PydanticObjectId

    class Settings:
        name = 'tags'
        indexes = [
            IndexModel(
                [('name', DESCENDING), ('user_id', DESCENDING)],
                unique=True
            )
        ]
