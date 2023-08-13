from collections import OrderedDict
import json
from datetime import datetime
from pprint import pformat

from sqlalchemy import DateTime, Integer, event, func
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class PrettyOrderedDict(OrderedDict):
    def formatted_repr(self, indent_level=0) -> str:
        indent: str = "\t" * indent_level
        items: list[str] = [
            f"\n{indent}\t{repr(k)}: {self.formatted_value_repr(v, indent_level)}"
            for k, v in self.items()
        ]
        return f"{indent}{{" + ",".join(items) + f"\n{indent}}}"

    def formatted_value_repr(self, value, indent_level):
        if isinstance(value, PrettyOrderedDict):
            return value.formatted_repr(indent_level)
        else:
            return repr(value)

    def __repr__(self) -> str:
        return self.formatted_repr(1)


class NamingDeclarativeMeta(DeclarativeMeta):
    def __init__(self, classname, bases, dict_):
        if "__name__" in dict_:
            classname = dict_["__name__"]
        super().__init__(classname, bases, dict_)


# To-JSON Mixin
class ToJsonMixin:
    def to_json(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(data_dict)


# Table Name Generation Mixin
class TableNameMixin:
    @declared_attr
    def __tablename__(cls):
        # If __tablename__ is not explicitly defined, generate it from the class name
        return cls.__name__.lower()


# ID Mixin
class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


# Timestamps Mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


# Base Model with only ToJsonMixin and TableNameMixin
class IntermediateBase(ToJsonMixin, TableNameMixin):
    __abstract__ = True

    def _dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        attributes = {
            c.name: getattr(self, c.name) if hasattr(self, c.name) else "Not Loaded"
            for c in self.__table__.columns
        }
        return f"{self.__class__.__name__}: {attributes}"


class BaseModel(IntermediateBase, IdMixin, TimestampMixin):
    def logger(self, logger, log_type, text, attr_list):
        dic = PrettyOrderedDict(
            [
                (attr, getattr(self, attr))
                for attr in attr_list
            ]
        )
        # dic = {: dic}
        log = getattr(logger, log_type)
        string: str = f"\n{self.__class__.__name__}{text}:\n{dic}"
        log(string)


Base = declarative_base(cls=BaseModel, metaclass=NamingDeclarativeMeta)

