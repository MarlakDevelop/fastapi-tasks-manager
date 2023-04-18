from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.domain import models, schemas


class ITaskRepository:
    async def fetch_ids(
        self,
        *,
        search: str = '',
        ids: list[int] | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> list[int]:
        pass

    async def fetch(self, *, ids: list[int]) -> list[schemas.TaskSchema]:
        pass

    async def fetch_count(self, *, search: str = '') -> int:
        pass

    async def fetch_one(self, *, id: int) -> schemas.TaskDetailSchema | None:
        pass

    async def insert(self, *, elements: list[schemas.CreateTaskSchema]) -> list[int]:
        pass

    async def insert_one(self, *, element: schemas.CreateTaskSchema) -> int:
        pass

    async def update(self, *, ids: list[int], element: schemas.UpdateTaskSchema) -> list[int]:
        pass

    async def update_one(self, *, id: int, element: schemas.UpdateTaskSchema) -> int:
        pass

    async def delete(self, *, ids: list[int]) -> list[int]:
        pass

    async def delete_one(self, *, id: int) -> int:
        pass
