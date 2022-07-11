from typing import Any, Dict
from datetime import datetime

from beanie import Document
from beanie.odm.fields import PydanticObjectId


class Resume(Document):
    timestamp_added: datetime = datetime.utcnow()
    filename: str
    raw_file: bytes
    content: Dict[Any, Any]
    user_id: PydanticObjectId
    tag_id: PydanticObjectId

    class Settings:
        name = 'resumes'
