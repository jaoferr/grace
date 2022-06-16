from pydantic import BaseModel

from datetime import datetime


class JobBase(BaseModel):
    name: str


class JobQuery(JobBase):
    user_id: int


class JobCreate(JobBase):
    user_id: int
    description: str

class JobCreateExternal(JobBase):
    description: str


class Job(JobBase):
    id: int
    user_id: int
    name: str
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True
