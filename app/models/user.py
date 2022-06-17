from typing import List, Optional

from beanie import Document, Indexed, Link
from beanie.odm.fields import PydanticObjectId

from app.models.resume import Resume
from app.models.tag import Tag

class User(Document):
    id: Optional[PydanticObjectId]
    email: str
    username: Indexed(str)
    password: str
    resumes: Optional[List[Link[Resume]]] = []
    tags: Optional[List[Link[Tag]]] = []
    
    class Settings:
        name = 'users'
