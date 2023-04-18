from enum import Enum


class TaskSignals(str, Enum):
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    DELETED = 'DELETED'
