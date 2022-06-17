from datetime import datetime

from beanie import Document, Indexed

class Job(Document):
    
    name: Indexed(str)
    description: str
    user_id: int
    timestamp_added: datetime
    
    class Settings:
        name = 'jobs'
    