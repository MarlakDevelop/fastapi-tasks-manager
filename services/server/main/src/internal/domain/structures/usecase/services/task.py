from src.internal.domain import schemas


class ITaskService:
    async def get_all(
        self,
        *,
        search: str = '',
        ids: list[int] | None = None
    ) -> list[schemas.TaskSchema]:
        pass

    async def get_paginated(
        self,
        *,
        search: str = '',
        ids: list[int] | None = None,
        limit: int | None = None,
        offset: int | None = None
    ) -> schemas.PaginationSchema[schemas.TaskSchema]:
        pass

    async def get_one(self, *, id: int) -> schemas.TaskDetailSchema | None:
        pass

    async def create_multiple(self, *, elements: list[schemas.CreateTaskSchema]) -> list[schemas.TaskSchema]:
        pass

    async def create_one(self, *, element: schemas.CreateTaskSchema) -> schemas.TaskDetailSchema:
        pass

    async def update_multiple(self, *, ids: list[int], element: schemas.UpdateTaskSchema) -> list[schemas.TaskSchema]:
        pass

    async def update_one(self, *, id: int, element: schemas.UpdateTaskSchema) -> schemas.TaskDetailSchema | None:
        pass

    async def delete_multiple(self, *, ids: list[int]) -> list[schemas.TaskSchema]:
        pass

    async def delete_one(self, *, id: int) -> schemas.TaskDetailSchema | None:
        pass

