import fastapi

from src.configs import pagination
from src.internal.domain import schemas, types
from src.internal.domain.structures.adapter.transport.http.controllers.task import ITaskController
from src.internal.domain.structures.adapter.transport.ws.broadcasters.task import ITaskBroadcaster
from src.internal.domain.structures.usecase.services.task import ITaskService
from .base import Controller
from ..dependencies.pagination import PaginationDependency
from ..dependencies.task import TaskDependency
from ..exceptions.task import TaskNotFoundException


class TaskController(ITaskController, Controller):
    task_dependency: TaskDependency = TaskDependency()
    pagination_dependency: PaginationDependency = PaginationDependency(per_page=pagination.get_settings().per_page)

    def __init__(self, *, task_service: ITaskService, task_broadcaster: ITaskBroadcaster):
        self.task_service = task_service
        self.task_broadcaster = task_broadcaster

    async def get_one(
        self,
        task_id: int = fastapi.Depends(task_dependency.get_id)
    ) -> schemas.TaskDetailSchema:
        task = await self.task_service.get_one(id=task_id)
        if task is None:
            raise TaskNotFoundException
        return task

    async def get(
        self,
        search: str = fastapi.Query(''),
        ids: list[int] | None = fastapi.Depends(task_dependency.get_optional_ids),
        limit_offset: tuple[int | None, int | None] = fastapi.Depends(pagination_dependency.get_pagination)
    ) -> schemas.PaginationSchema[schemas.TaskSchema] | list[schemas.TaskSchema]:
        limit, offset = limit_offset
        if limit is not None and offset is not None:
            tasks = await self.task_service.get_paginated(search=search, ids=ids, limit=limit, offset=offset)
        else:
            tasks = await self.task_service.get_all(search=search, ids=ids)
        return tasks

    async def post_one(self, element: schemas.CreateTaskSchema) -> schemas.TaskDetailSchema:
        task = await self.task_service.create_one(element=element)
        await self.task_broadcaster.send_pydantic_to_all(
            data=schemas.WebSocketMessageSchema(
                type=types.TaskSignals.CREATED,
                data=[schemas.TaskSchema(**task.dict())]
            )
        )
        return task

    async def post(
        self,
        elements: list[schemas.CreateTaskSchema] = fastapi.Body(..., min_items=1, max_items=20)
    ) -> list[schemas.TaskSchema]:
        tasks = await self.task_service.create_multiple(elements=elements)
        await self.task_broadcaster.send_pydantic_to_all(
            data=schemas.WebSocketMessageSchema(
                type=types.TaskSignals.CREATED,
                data=tasks
            )
        )
        return tasks

    async def patch_one(
        self,
        id: int = fastapi.Depends(task_dependency.get_id),
        element: schemas.UpdateTaskSchema = fastapi.Body(...)
    ) -> schemas.TaskDetailSchema:
        task = await self.task_service.update_one(id=id, element=element)
        if task is None:
            raise TaskNotFoundException
        await self.task_broadcaster.send_pydantic_to_all(
            data=schemas.WebSocketMessageSchema(
                type=types.TaskSignals.UPDATED,
                data=[schemas.TaskSchema(**task.dict())]
            )
        )
        return task

    async def patch(
        self,
        ids: list[int] = fastapi.Depends(task_dependency.get_ids),
        element: schemas.UpdateTaskSchema = fastapi.Body(...)
    ) -> list[schemas.TaskSchema]:
        tasks = await self.task_service.update_multiple(ids=ids, element=element)
        await self.task_broadcaster.send_pydantic_to_all(
            data=schemas.WebSocketMessageSchema(
                type=types.TaskSignals.UPDATED,
                data=tasks
            )
        )
        return tasks

    async def delete_one(
        self,
        id: int = fastapi.Depends(task_dependency.get_id),
    ) -> schemas.TaskDetailSchema:
        task = await self.delete_one(id=id)
        if task is None:
            raise TaskNotFoundException
        await self.task_broadcaster.send_pydantic_to_all(
            data=schemas.WebSocketMessageSchema(
                type=types.TaskSignals.DELETED,
                data=[schemas.TaskSchema(**task.dict())]
            )
        )
        return task

    async def delete(
        self,
        ids: list[int] = fastapi.Depends(task_dependency.get_ids)
    ) -> list[schemas.TaskSchema]:
        tasks = await self.task_service.delete_multiple(ids=ids)
        await self.task_broadcaster.send_pydantic_to_all(
            data=schemas.WebSocketMessageSchema(
                type=types.TaskSignals.DELETED,
                data=tasks
            )
        )
        return tasks
