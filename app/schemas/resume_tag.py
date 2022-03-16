from pydantic import BaseModel
from typing import List
from app.schemas import Resume

class ResumeTagBase(BaseModel):
    user_id: int
    tag: str


class ResumeTagCreate(ResumeTagBase):
    pass

class ResumeTag(ResumeTagBase):
    id: int
    resumes: List[Resume]

    class Config:
        orm_mode = True
