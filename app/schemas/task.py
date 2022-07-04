from pydantic import BaseModel


class TaskOut(BaseModel):
    id: str
    status: str
