from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ResumeIndexBase(BaseModel):
    pass


class ResumeIndexCreate(ResumeIndexBase):
    object_id: str
    user_id: int
    filename: str
    batch_id: str

class Resume(ResumeIndexBase):
    id: int
    object_id: str
    user_id: int
    timestamp: datetime
    filename: str
    batch_id: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    resumes: list[Resume]

    class Config:
        orm_mode = True
