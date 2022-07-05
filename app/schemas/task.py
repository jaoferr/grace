from pydantic import BaseModel


class TaskOut(BaseModel):
    id: str
    status: str

class TaskStatus(TaskOut):
    progress: float
