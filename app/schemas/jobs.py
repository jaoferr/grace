from pydantic import BaseModel


class JobBase(BaseModel):
    description: str


class JobQuery(JobBase):
    user_id: int


class JobCreate(JobBase):
    user_id: int


class JobCreateExternal(JobBase):
    pass


class Job(JobBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True
