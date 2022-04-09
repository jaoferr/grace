from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas import Resume


class BatchBase(BaseModel):
    id: str
    user_id: str


class BatchCreate(BatchBase):
    pass


class Batch(BatchBase):
    timestamp: datetime
    item_count: int
    resumes: List[Resume]

    class Config:
        orm_mode = True
