from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    pass


class User(UserBase):

    class Config:
        orm_mode = True
        