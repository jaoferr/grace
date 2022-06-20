from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel
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

class Tag(TagBase):
    id: PydanticObjectId
    name: str
    description: Optional[str]
    timestamp: datetime
    resume_count: int
    disk_size: int
