from datetime import datetime
from typing import List

from beanie import Document, Indexed, Link

from app.models.resume import Resume

class Tag(Document):
    
    name: Indexed(str)
    description: str
    timestamp_added: datetime
    user_id: int
    resumes: List[Link[Resume]]

    class Settings:
        name = 'tags'
