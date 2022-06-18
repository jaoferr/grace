from datetime import datetime

from beanie import Document, Indexed
from beanie.odm.fields import PydanticObjectId
from pymongo.operations import IndexModel
from pymongo import DESCENDING

class Job(Document):
    
    name: str
    description: str
    user_id: PydanticObjectId
    timestamp_added: datetime = datetime.utcnow()

    class Settings:
        name = 'jobs'
        indexes = [
            IndexModel(
                [('name', DESCENDING), ('user_id', DESCENDING)],
                unique=True    
            )
        ]
    