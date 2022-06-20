from typing import List, Optional

from beanie import Document, Indexed, Link

from app.models.job import Job
from app.models.tag import Tag

class User(Document):
    email: Indexed(str, unique=True)
    username: Indexed(str)
    password: str
    jobs: Optional[List[Link[Job]]] = []
    tags: Optional[List[Link[Tag]]] = []

    class Settings:
        name = 'users'
