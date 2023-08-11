import json
from datetime import datetime
from pprint import pformat

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class NamingDeclarativeMeta(DeclarativeMeta):
    def __init__(self, classname, bases, dict_):
        if "__name__" in dict_:
            classname = dict_["__name__"]
        super().__init__(classname, bases, dict_)


# 1. To-JSON Mixin
class ToJsonMixin:
    def to_json(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(data_dict)


# 2. Table Name Generation Mixin
class TableNameMixin:
    @declared_attr
    def __tablename__(cls):
        # If __tablename__ is not explicitly defined, generate it from the class name
        return cls.__name__.lower()


# 3. Base Model with Mixins included
class BaseModel(ToJsonMixin, TableNameMixin):
    __abstract__ = True  # Ensure that BaseModel is not treated as a model for a table

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def _dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {pformat(self._dict())}"


Base = declarative_base(cls=BaseModel, metaclass=NamingDeclarativeMeta)
