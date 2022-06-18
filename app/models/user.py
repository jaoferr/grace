from typing import List, Optional

from pydantic import Field
from beanie import Document, Indexed, Link

from app.models.resume import Resume
from app.models.tag import Tag

class User(Document):

    email: str
    username: Indexed(str)
    password: str
    resumes: Optional[List[Link[Resume]]] = []
    tags: Optional[List[Link[Tag]]] = []
    
    class Settings:
        name = 'users'
