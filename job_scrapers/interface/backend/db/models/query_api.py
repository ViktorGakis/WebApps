from collections import OrderedDict
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from ..base import Base


class Query_Api(Base):
    __tablename__: str = "query_api"
    # __table_args__: tuple[dict[str, bool]] = {"extend_existing": True}
    id: Column = Column("id", Integer(), primary_key=True)
    query: Column = Column("query", String(), default=None)
    location: Column = Column("location", String(), default=None)
    days: Column = Column("days", Integer(), default=None)
    num_pages: Column = Column("num_pages", Integer(), default=None)
    total_hits: Column = Column("total_hits", Integer(), default=None)
    actual_hits: Column = Column("actual_hits", Integer(), default=None)
    current_page: Column = Column("current_page", String(), default=None)
    url: Column = Column("url", String(), default=None)
    dateLog: Column = Column(
        "dateLog", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def __init__(
        self,
        url: Optional[String],
        query: Optional[String],
        location: Optional[String],
        num_pages: Optional[Integer] = None,
        total_hits: Optional[Integer] = None,
        current_page: Optional[Integer] = None,
        actual_hits: Optional[Integer] = None,
        days: Optional[Integer] = None,
    ):
        self.num_pages = num_pages
        self.total_hits = total_hits
        self.current_page = current_page
        self.query = query
        self.location = location
        self.url = url
        self.actual_hits = actual_hits
        self.days = days

    def serialize(self) -> dict:
        return OrderedDict(
            {
                "id": self.id,
                "query": self.query,
                "location": self.location,
                "days": self.days,
                "num_pages": self.num_pages,
                "total_hits": self.total_hits,
                "actual_hits": self.actual_hits,
                "current_page": self.current_page,
                "url": self.url,
                "dateLog": self.dateLog,
            }
        )

    def __repr__(self) -> str:
        return f"{self.serialize()}"
