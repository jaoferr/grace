from typing import List

from beanie import Document, Indexed, Link

from app.models.resume import Resume
from app.models.tag import Tag

class User(Document):
    
    id: int
    email: str
    username: Indexed(str)
    password: str
    resumes: List[Link[Resume]]
    tags: List[Link[Tag]]
    
    class Settings:
        name = 'users'