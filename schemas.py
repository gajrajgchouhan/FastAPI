from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    is_completed: bool


class TaskModel(TaskBase):
    id: int
    title: str
    is_completed: bool

    class Config:
        orm_mode = True


class CreateTaskModel(BaseModel):
    title: str

    class Config:
        orm_mode = True


class GetTaskModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UpdateTaskModel(BaseModel):
    title: str
    is_completed: bool

    class Config:
        orm_mode = True
