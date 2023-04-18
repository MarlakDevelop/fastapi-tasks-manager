from sqlalchemy import select, func, insert, update, delete

from src.internal.adapter.data.repositories.base import Repository
from src.internal.domain import models
from src.internal.domain import schemas
from src.internal.domain.structures.adapter.data.repositories.task import ITaskRepository


class TaskRepository(ITaskRepository, Repository):
    async def fetch_ids(
        self,
        *,
        search: str = '',
        ids: list[int] | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> list[int]:
        session = await anext(self.get_db_session())
        search = f'%{search}%'
        stmt = select(models.Task.id)\
            .filter((models.Task.name.ilike(search)) | (models.Task.text.ilike(search)))
        if ids is not None:
            stmt = stmt.filter(models.Task.id.in_(ids))
        if limit is not None and offset is not None:
            stmt = stmt.limit(limit)\
                .offset(offset)
        stmt = stmt.order_by(models.Task.updated_at.desc())
        result = await session.execute(stmt)
        ids = result.scalars()
        return ids

    async def fetch(self, *, ids: list[int]) -> list[schemas.TaskSchema]:
        session = await anext(self.get_db_session())
        stmt = select(models.Task)\
            .with_only_columns(
                models.Task.id, models.Task.name, models.Task.is_complete,
                models.Task.deadline_at, models.Task.created_at, models.Task.updated_at
            )\
            .filter(models.Task.id.in_(ids))\
            .order_by(models.Task.updated_at.desc(), models.Task.created_at.desc())
        result = await session.execute(stmt)
        rows = result.all()
        return list(map(lambda row: schemas.TaskSchema.from_orm(row), rows))

    async def fetch_count(self, *, search: str = '') -> int:
        session = await anext(self.get_db_session())
        search = f'%{search}%'
        stmt = select(func.count())\
            .select_from(models.Task)\
            .filter((models.Task.name.ilike(search)) | (models.Task.text.ilike(search)))
        result = await session.execute(stmt)
        count: int = result.scalar()
        return count

    async def fetch_one(self, *, id: int) -> schemas.TaskDetailSchema | None:
        session = await anext(self.get_db_session())
        stmt = select(models.Task)\
            .filter(models.Task.id == id)
        result = await session.execute(stmt)
        row = result.one_or_none()
        if row is None:
            return None
        return schemas.TaskSchema.from_orm(row)

    async def insert(self, *, elements: list[schemas.CreateTaskSchema]) -> list[int]:
        session = await anext(self.get_db_session())
        stmt = insert(models.Task)\
            .values(list(map(lambda element: element.dict(), elements)))\
            .returning(models.Task.id)
        result = await session.execute(stmt)
        await session.commit()
        tasks_ids = result.scalars()
        return tasks_ids

    async def insert_one(self, *, element: schemas.CreateTaskSchema) -> int:
        session = await anext(self.get_db_session())
        stmt = insert(models.Task)\
            .values(element.dict())\
            .returning(models.Task.id)
        result = await session.execute(stmt)
        await session.commit()
        task_id = result.scalar()
        return task_id

    async def update(self, *, ids: list[int], element: schemas.UpdateTaskSchema) -> list[int]:
        session = await anext(self.get_db_session())
        data = {k: v for k, v in element.dict().items() if v is not None}
        stmt = update(models.Task)\
            .where(models.Task.id.in_(ids))\
            .values(data)\
            .returning(models.Task.id)
        result = await session.execute(stmt)
        await session.commit()
        tasks_ids = result.scalars()
        return tasks_ids

    async def update_one(self, *, id: int, element: schemas.UpdateTaskSchema) -> int | None:
        session = await anext(self.get_db_session())
        data = {k: v for k, v in element.dict().items() if v is not None}
        stmt = update(models.Task)\
            .where(models.Task.id == id)\
            .values(data)\
            .returning(models.Task.id)
        result = await session.execute(stmt)
        await session.commit()
        task_id = result.scalar()
        return task_id

    async def delete(self, *, ids: list[int]) -> list[int]:
        session = await anext(self.get_db_session())
        stmt = delete(models.Task)\
            .where(models.Task.id.in_(ids))\
            .returning(models.Task.id)
        result = await session.execute(stmt)
        await session.commit()
        tasks_ids = result.scalars()
        return tasks_ids

    async def delete_one(self, *, id: int) -> int | None:
        session = await anext(self.get_db_session())
        stmt = delete(models.Task)\
            .where(models.Task.id == id)\
            .returning(models.Task.id)
        result = await session.execute(stmt)
        await session.commit()
        task_id = result.scalar()
        return task_id
