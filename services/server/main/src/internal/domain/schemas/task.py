import datetime

import pydantic


class CreateTaskSchema(pydantic.BaseModel):
    name: str = pydantic.Field(..., min_length=1, max_length=100)
    text: str = pydantic.Field(..., max_length=1000)
    deadline_at: datetime.datetime = pydantic.Field(..., alias='deadlineAt')


class UpdateTaskSchema(pydantic.BaseModel):
    name: str | None = pydantic.Field(None, min_length=1, max_length=100)
    text: str | None = pydantic.Field(None, max_length=1000)
    deadline_at: datetime.datetime | None = pydantic.Field(None, alias='deadlineAt')
    is_complete: str | None = pydantic.Field(None, alias='isComplete')


class TaskSchema(pydantic.BaseModel):
    id: int
    name: str
    is_complete: bool = pydantic.Field(..., alias='isComplete')
    deadline_at: datetime.datetime = pydantic.Field(..., alias='deadlineAt')
    created_at: datetime.datetime = pydantic.Field(..., alias='createdAt')
    updated_at: datetime.datetime | None = pydantic.Field(..., alias='updatedAt')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TaskDetailSchema(TaskSchema):
    text: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
