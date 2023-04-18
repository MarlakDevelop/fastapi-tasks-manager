import enum

import fastapi
import pydantic

from .base import Dependency


class PaginationType(int, enum.Enum):
    LIMIT_OFFSET = 1
    PAGED = 2


class PaginationDependency(Dependency):
    def __init__(self, per_page: int):
        self.per_page = per_page

    async def get_pagination(
        self,
        limit: pydantic.PositiveInt | None = fastapi.Query(None),
        offset: pydantic.NonNegativeInt | None = fastapi.Query(None),
        page_size: pydantic.PositiveInt | None = fastapi.Query(None, alias='pageSize'),
        page: pydantic.PositiveInt | None = fastapi.Query(None)
    ) -> tuple[int | None, int | None]:
        if limit is not None or offset is not None:
            return self._transform_to_limit_offset(pagination=(limit, offset), _type=PaginationType.LIMIT_OFFSET)
        if page_size is not None or page is not None:
            return self._transform_to_limit_offset(pagination=(page_size, page), _type=PaginationType.PAGED)
        return None, None

    def _transform_to_limit_offset(self, pagination, _type: PaginationType) -> tuple[int, int]:
        match _type:
            case PaginationType.LIMIT_OFFSET:
                limit, offset = pagination
                if limit is None:
                    limit = self.per_page
                if offset is None:
                    offset = 0
                return pagination
            case PaginationType.PAGED:
                page_size, page = pagination
                if page_size is None:
                    page_size = self.per_page
                if page is None:
                    page = 1
                return page_size, (page - 1) * page_size
