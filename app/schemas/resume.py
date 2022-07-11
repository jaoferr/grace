from typing import Any, Dict

from pydantic import BaseModel
from beanie.odm.fields import PydanticObjectId


class ResumeBase(BaseModel):
    pass


class ResumeCreate(ResumeBase):
    user_id: PydanticObjectId
    tag_id: PydanticObjectId
    raw_file: bytes
    filename: str
    content: Dict[Any, Any]
