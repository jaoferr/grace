from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId

from datetime import datetime


class JobBase(BaseModel):
    name: str


class JobQuery(JobBase):
    user_id: PydanticObjectId


class JobCreate(JobBase):
    user_id: PydanticObjectId
    description: str

class JobCreateExternal(JobBase):
    description: str


class JobOut(JobBase):
    id: PydanticObjectId = Field(..., alias='_id')
    user_id: PydanticObjectId
    name: str
    description: str
    timestamp_added: datetime

    class Config:
        orm_mode = True
