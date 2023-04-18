import fastapi

from .base import Dependency


class TaskDependency(Dependency):
    async def get_id(self, task_id: int = fastapi.Path(..., alias='taskId')) -> int:
        return task_id

    async def get_ids(self, tasks_ids: list[int] = fastapi.Query(..., alias='tasksIds')) -> list[int]:
        return tasks_ids

    async def get_optional_ids(self, tasks_ids: list[int] | None = fastapi.Query(None, alias='tasksIds')) -> list[int]:
        return tasks_ids
