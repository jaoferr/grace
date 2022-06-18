from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: PydanticObjectId = Field(..., alias='_id')


class User(UserBase):

    class Config:
        orm_mode = True
        