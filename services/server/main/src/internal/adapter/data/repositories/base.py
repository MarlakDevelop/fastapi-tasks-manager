from typing import Callable, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    def __init__(self, get_db_session: Callable[[], AsyncIterator[AsyncSession]]):
        self.get_db_session = get_db_session
