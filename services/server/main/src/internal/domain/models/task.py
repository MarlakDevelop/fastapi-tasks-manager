import sqlalchemy

from .base import Base, IdMixin, TimestampsMixin


class Task(IdMixin, TimestampsMixin, Base):
    __tablename__ = 'tasks'

    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(1000), nullable=False)
    is_complete = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    deadline_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
