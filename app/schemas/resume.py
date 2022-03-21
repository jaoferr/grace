from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class ResumeBase(BaseModel):
    object_id: str


class ResumeCreateExternal(BaseModel):
    tag: str


class ResumeCreate(ResumeBase):
    user_id: int
    filename: str
    batch_id: str
    tag_id: int
    content: Dict[Any, Any]


class Resume(ResumeBase):
    id: int
    user_id: int
    tag_id: int
    timestamp: datetime
    filename: str
    batch_id: str
    content: Optional[Dict[Any, Any]]

    class Config:
        orm_mode = True


class ResumeBatch(BaseModel):
    user_id: int
    resume_count: int
    tag: str
    files: List[Resume]


class ResumeContent(BaseModel):
    content_keys: List[Any]
