from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from app.schemas import Resume


class ResumeTagBase(BaseModel):
    user_id: int
    name: str
    description: Optional[str]

class ResumeTagQuery(ResumeTagBase):
    pass

class ResumeTagCreateExternal(BaseModel):
    name: str
    description: Optional[str]

class ResumeTagCreate(ResumeTagBase):
    pass

class ResumeTag(ResumeTagBase):
    id: int
    # resumes: List[Resume]
    name: str
    description: Optional[str]
    timestamp: datetime
    resume_count: int
    disk_size: int

    class Config:
        orm_mode = True
