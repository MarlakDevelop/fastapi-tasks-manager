from typing import TypeVar, Generic

import pydantic
from pydantic import BaseModel
from pydantic.generics import GenericModel


class DetailResponseSchema(BaseModel):
    detail: str


PaginatableT = TypeVar('PaginatableT')


class PaginationSchema(GenericModel, Generic[PaginatableT]):
    list: list[PaginatableT]
    total_count: int = pydantic.Field(..., alias='totalCount')

    class Config:
        allow_population_by_field_name = True


WebSocketMessageDataT = TypeVar('WebSocketMessageDataT')


class WebSocketMessageSchema(GenericModel, Generic[WebSocketMessageDataT]):
    type: str
    data: WebSocketMessageDataT
