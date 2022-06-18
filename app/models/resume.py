from datetime import datetime

from beanie import Document
from beanie.odm.fields import PydanticObjectId

class Resume(Document):
    
    timestamp_added: datetime = datetime.utcnow()
    filename: str
    content: str
    user_id: PydanticObjectId
    tag_id: PydanticObjectId
    
    class Settings:
        name = 'resumes'