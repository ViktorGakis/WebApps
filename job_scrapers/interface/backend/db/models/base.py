from pprint import pformat

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


class NamingDeclarativeMeta(DeclarativeMeta):
    def __init__(self, classname, bases, dict_):
        if "__name__" in self.__dict__:
            self.__name__ = classname = self.__dict__["__name__"]
        DeclarativeMeta.__init__(self, classname, bases, dict_)

    def _dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {pformat(self._dict())}"


Base = declarative_base(metaclass=NamingDeclarativeMeta)
