from collections import OrderedDict

from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql import func

from ..base import Base


class SubQuery(Base):
    __tablename__: str = "subquery"
    # __table_args__: tuple[dict[str, bool]] = {"extend_existing": True}
    id: Column = Column("id", Integer(), primary_key=True)
    clientClassification: Column = Column("clientClassification", String())
    pageTitle: Column = Column("pageTitle", String(), default=None)
    pageDescription: Column = Column("pageDescription", String(), default=None)
    pageList: Column = Column("pageList", String(), default=None)
    numPages: Column = Column("numPages", Integer(), default=None)
    totalHits: Column = Column("totalHits", Integer(), default=None)
    searchQuery: Column = Column("searchQuery", String(), default=None)
    url: Column = Column("url", String(), default=None)
    queryId: Column = Column("queryId", Integer(), default=None)
    dateLog: Column = Column(
        "date_log", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def __init__(
        self,
        clientClassification=None,
        pageTitle=None,
        pageDescription=None,
        pageList=None,
        numPages=None,
        totalHits=None,
        searchQuery=None,
        url=None,
        queryId=None,
    ):
        self.clientClassification = clientClassification
        self.pageTitle = pageTitle
        self.pageDescription = pageDescription
        self.pageList = pageList
        self.numPages = numPages
        self.totalHits = totalHits
        self.searchQuery = searchQuery
        self.url = url
        self.queryId = queryId

    def serialize(self) -> dict:
        return OrderedDict(
            {
                "clientClassification": self.clientClassification,
                "pageTitle": self.pageTitle,
                "pageDescription": self.pageDescription,
                "pageList": self.pageList,
                "numPages": self.numPages,
                "totalHits": self.totalHits,
                "searchQuery": self.searchQuery,
                "queryId": self.queryId,
                "dateLog": self.dateLog,
            }
        )

    def __repr__(self) -> str:
        return f"{self.serialize()}"
