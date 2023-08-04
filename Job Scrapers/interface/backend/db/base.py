from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


class NamingDeclarativeMeta(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        if "__name__" in cls.__dict__:
            cls.__name__ = classname = cls.__dict__["__name__"]
        DeclarativeMeta.__init__(cls, classname, bases, dict_)


Base = declarative_base(metaclass=NamingDeclarativeMeta)
