import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class IdMixin:
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)


class CreatedAtMixin:
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True), server_default=func.now())


class UpdatedAtMixin:
    updated_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True), nullable=True, default=None, onupdate=func.now())


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
