import dataclasses
from functools import lru_cache

from src.configs.environment import get_environment_variables


env = get_environment_variables()


@dataclasses.dataclass
class TasksPaginationSettings:
    per_page: int = env.PAGINATION_TASKS_PAGE_SIZE


@lru_cache
def get_settings():
    return TasksPaginationSettings()
