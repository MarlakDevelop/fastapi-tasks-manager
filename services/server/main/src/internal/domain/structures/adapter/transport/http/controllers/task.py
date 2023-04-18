from src.internal.domain import schemas


class ITaskController:
    async def get_one(self, task_id: int) -> schemas.TaskDetailSchema:
        pass

    async def get(
        self, search: str, ids: list[int] | None, limit_offset: tuple[int | None, int | None]
    ) -> schemas.PaginationSchema[schemas.TaskSchema] | list[schemas.TaskSchema]:
        pass

    async def post_one(self, element: schemas.CreateTaskSchema) -> schemas.TaskDetailSchema:
        pass

    async def post(self, elements: list[schemas.CreateTaskSchema]) -> list[schemas.TaskSchema]:
        pass

    async def patch_one(self, id: int, element: schemas.UpdateTaskSchema) -> schemas.TaskDetailSchema:
        pass

    async def patch(self, ids: list[int], element: schemas.UpdateTaskSchema) -> list[schemas.TaskSchema]:
        pass

    async def delete_one(self, id: int) -> schemas.TaskDetailSchema:
        pass

    async def delete(self, ids: list[int]) -> list[schemas.TaskSchema]:
        pass
