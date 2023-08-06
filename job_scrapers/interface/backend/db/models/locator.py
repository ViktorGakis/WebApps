from collections import OrderedDict

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from ..base import Base


class Locator(Base):
    __tablename__: str = "locator"
    # __table_args__: dict[str, bool] = {"extend_existing": True}
    id: Column = Column("id", Integer(), primary_key=True)
    job_location: Column = Column("job_location", String(), default=None)
    goog_location: Column = Column("goog_location", String(), default=None)
    state_district: Column = Column("state_district", String(), default=None)
    county: Column = Column("county", String(), default=None)  
    municipality: Column = Column("municipality", String(), default=None)      
    region: Column = Column("region", String(), default=None)
    
    city: Column = Column("city", String(), default=None)
    country: Column = Column("country", String(), default=None)
    
    cc: Column = Column("cc", String(), default=None)
        
    lat: Column = Column("lat", String(), default=None)
    lon: Column = Column("lon", String(), default=None)
    url: Column = Column("url", String(), default=None) 
    Date_log: Column = Column(
        "Date_log", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def serialize(self) -> dict:
        return OrderedDict(
            {
                "id": self.id,
                "job_location": self.job_location,
                "goog_location": self.goog_location,
                "state_district": self.state_district,
                "county": self.county,
                "municipality": self.municipality,
                "region": self.region,
                "city": self.city,
                "country": self.country,
                "lat": self.lat,
                "lon": self.lon,
                "url": self.url,
                "Date_log": self.Date_log,
            }
        )

    def __repr__(self) -> str:
        return f"{self.serialize()}"
