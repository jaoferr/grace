from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Form
from pydantic import BaseModel
from beanie.odm.fields import PydanticObjectId

class ResumeBase(BaseModel):
    pass


class ResumeCreate(ResumeBase):
    user_id: int
    tag_id: int
    filename: str
    content: Dict[Any, Any]
