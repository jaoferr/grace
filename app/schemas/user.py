from pydantic import BaseModel
from typing import List
from .resume_tag import ResumeTag


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    resume_count: int

    class Config:
        orm_mode = True
        