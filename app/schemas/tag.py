from typing import List
from datetime import datetime

from pydantic import BaseModel

from app.schemas import Resume


class ResumeTagBase(BaseModel):
    user_id: int
    tag: str

class ResumeTagQuery(ResumeTagBase):
    pass

class ResumeTagCreateExternal(BaseModel):
    tag: str

class ResumeTagCreate(ResumeTagBase):
    pass

class ResumeTag(ResumeTagBase):
    id: int
    # resumes: List[Resume]
    tag: str
    timestamp: datetime
    resume_count: int
    disk_size: int

    class Config:
        orm_mode = True
