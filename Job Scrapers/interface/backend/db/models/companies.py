from collections import OrderedDict
from pprint import pformat

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from ..base import Base


class Company(Base):
    __tablename__: str = "companies"
    id: Column = Column("id", Integer(), primary_key=True)
    name: Column = Column("name", String(), default=None)
    company_id: Column = Column("company_id", String(), default=None)
    employees_in: Column = Column("employees_in", Integer(), default=None)
    followers: Column = Column("followers", Integer(), default=None)
    employees: Column = Column("employees", Integer(), default=None)
    num_aff: Column = Column("num_aff", Integer(), default=None)
    aff: Column = Column("aff", String(), default=None)
    industries: Column = Column("industries", String(), default=None)
    industryIds: Column = Column("industryIds", String(), default=None)
    headquarters: Column = Column("headquarters", String(), default=None)
    location: Column = Column("location", String(), default=None)
    organization_type: Column = Column("organization_type", String(), default=None)
    specialties: Column = Column("specialties", String(), default=None)
    website: Column = Column("website", String(), default=None)
    url_in: Column = Column("url_in", String(), default=None)
    street_adress: Column = Column("street_adress", String(), default=None)
    address_region: Column = Column("address_region", String(), default=None)
    address_locality: Column = Column("address_locality", String(), default=None)
    address_country: Column = Column("address_country", String(), default=None)
    postal_code: Column = Column("postal_code", String(), default=None)
    descr: Column = Column("descr", String(), default=None)
    fav: Column = Column("fav", Integer(), default=0)
    status: Column = Column("status", Integer(), default=None)
    Date_log: Column = Column(
        "Date_log", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    # __table_args__: dict[str, bool] = {"extend_existing": True}
    def serialize(self) -> dict:
        return OrderedDict(
            {
                "id": self.id,
                "name": self.name,
                "company_id": self.company_id,
                "employees_in": self.employees_in,
                "followers": self.followers,
                "employees": self.employees,
                "num_aff": self.num_aff,
                "aff": self.aff,
                "industries": self.industries,
                "industryIds": self.industryIds,
                "headquarters": self.headquarters,
                "location": self.location,
                "organization_type": self.organization_type,
                "specialties": self.specialties,
                "website": self.website,
                "url_in": self.url_in,
                "street_adress": self.street_adress,
                "address_region": self.address_region,
                "address_locality": self.address_locality,
                "address_country": self.address_country,
                "postal_code": self.postal_code,
                "descr": self.descr,
                "fav": self.fav,
                "status": self.status,
                "Date_log": self.Date_log,
            }
        )

    def __repr__(self) -> str:
        return pformat(self.serialize())
