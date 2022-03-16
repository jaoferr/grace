from pydantic import BaseModel
from datetime import datetime
from typing import List
from app import schemas


class BatchBase(BaseModel):
    id: str
    user_id: str


class BatchCreate(BatchBase):
    pass


class Batch(BatchBase):
    timestamp: datetime
    item_count: int
    resumes: List[schemas.Resume]

    class Config:
        orm_mode = True