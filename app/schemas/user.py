from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: PydanticObjectId

    class Config:
        # orm_mode = True
        json_encoder = {
            PydanticObjectId: lambda x: str(x)
        }

class User(UserBase):

    class Config:
        orm_mode = True
        