from src.internal.domain import schemas
from src.internal.domain.structures.adapter.data.repositories.task import ITaskRepository
from src.internal.domain.structures.usecase.services.task import ITaskService
from src.internal.usecase.services.base import Service


class TaskService(ITaskService, Service):
    def __init__(self, task_repository: ITaskRepository,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_repository = task_repository

    async def get_all(
        self,
        *,
        search: str = '',
        ids: list[int] | None = None
    ) -> list[schemas.TaskSchema]:
        ids = await self.task_repository.fetch_ids(search=search, ids=ids)
        elements = await self.task_repository.fetch(ids=ids)
        return elements

    async def get_paginated(
        self,
        *,
        search: str = '',
        ids: list[int] | None = None,
        limit: int | None = None,
        offset: int | None = None
    ) -> schemas.PaginationSchema[schemas.TaskSchema]:
        ids = await self.task_repository.fetch_ids(search=search, ids=ids, limit=limit, offset=offset)
        elements = await self.task_repository.fetch(ids=ids)
        total_count = await self.task_repository.fetch_count(search=search)
        return schemas.PaginationSchema[schemas.TaskSchema](list=elements, total_count=total_count)

    async def get_one(
        self,
        *,
        id: int
    ) -> schemas.TaskDetailSchema | None:
        element = await self.task_repository.fetch_one(id=id)
        return element

    async def create_multiple(
        self,
        *,
        elements: list[schemas.CreateTaskSchema]
    ) -> list[schemas.TaskSchema]:
        ids = await self.task_repository.insert(elements=elements)
        elements = await self.task_repository.fetch(ids=ids)
        return elements

    async def create_one(
        self,
        *,
        element: schemas.CreateTaskSchema
    ) -> schemas.TaskDetailSchema:
        id = await self.task_repository.insert_one(element=element)
        element = await self.task_repository.fetch_one(id=id)
        return element

    async def update_multiple(
        self,
        *,
        ids: list[int],
        element: schemas.UpdateTaskSchema
    ) -> list[schemas.TaskSchema]:
        ids = await self.task_repository.update(ids=ids, element=element)
        elements = await self.task_repository.fetch(ids=ids)
        return elements

    async def update_one(
        self,
        *,
        id: int,
        element: schemas.UpdateTaskSchema
    ) -> schemas.TaskDetailSchema | None:
        id = await self.task_repository.update_one(id=id, element=element)
        if id is None:
            return None
        element = await self.task_repository.fetch_one(id=id)
        return element

    async def delete_multiple(
        self,
        *,
        ids: list[int]
    ) -> list[schemas.TaskSchema]:
        elements = await self.task_repository.fetch(ids=ids)
        await self.task_repository.delete(ids=ids)
        return elements

    async def delete_one(
        self,
        *,
        id: int
    ) -> schemas.TaskDetailSchema | None:
        element = await self.task_repository.fetch_one(id=id)
        if element is None:
            return None
        await self.task_repository.delete_one(id=id)
        return element
