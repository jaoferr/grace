from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId


class TagBase(BaseModel):
    user_id: PydanticObjectId
    name: str
    description: Optional[str]


class TagQuery(TagBase):
    pass


class TagCreateExternal(BaseModel):
    name: str
    description: Optional[str]


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: PydanticObjectId = Field(..., alias='_id')
    name: str
    description: Optional[str]
    timestamp_added: datetime
    resume_count: Optional[int]
    disk_size: Optional[int]
