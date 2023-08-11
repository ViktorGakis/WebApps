from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..base import Base


class Request(Base):
    __tablename__: str = "jobsch_requests"
    # __table_args__: tuple[dict[str, bool]] = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Optional[int]]
    query: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    days: Mapped[Optional[int]]
    num_pages: Mapped[Optional[int]]
    total_hits: Mapped[Optional[int]]
    actual_hits: Mapped[Optional[int]]
    duplicates: Mapped[Optional[int]]
    current_page: Mapped[Optional[int]]
    url: Mapped[Optional[str]]
    date_log: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    sub_requests = relationship("Sub_Request", back_populates="request")
    jobs = relationship("Job", back_populates="request")


class Sub_Request(Base):
    __tablename__: str = "jobsch_sub_requests"
    # ... other code ...ting": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Optional[int]]
    query: Mapped[Optional[str]]  # Not a foreign key"requests.query"))
    location: Mapped[Optional[str]]  # Not a foreign keyey("requests.location"))
    days: Mapped[Optional[int]]  # Not a foreign keyrequests.days"))
    num_pages: Mapped[Optional[int]]
    total_hits: Mapped[Optional[int]]
    actual_hits: Mapped[Optional[int]]
    duplicates: Mapped[Optional[int]]
    current_page: Mapped[Optional[int]]
    url: Mapped[Optional[str]]
    request_id: Mapped[int] = mapped_column(ForeignKey("jobsch_requests.id"))

    date_log: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    request = relationship("Request", back_populates="sub_requests")
    jobs = relationship("Job", back_populates="sub_request")


class Job(Base):
    __tablename__: str = "jobsch_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    publication_date: Mapped[Optional[str]]
    company_name: Mapped[Optional[str]]
    place: Mapped[Optional[str]]
    is_active: Mapped[Optional[bool]]
    preview: Mapped[Optional[str]]
    company_logo_file: Mapped[Optional[str]]
    job_id: Mapped[Optional[str]]
    slug: Mapped[Optional[str]]
    company_slug: Mapped[Optional[str]]
    company_id: Mapped[Optional[int]]
    company_segmentation: Mapped[Optional[str]]
    employment_position_ids: Mapped[Optional[str]]
    employment_grades: Mapped[Optional[str]]
    is_paid: Mapped[Optional[bool]]
    work_experience: Mapped[Optional[str]]
    language_skills: Mapped[Optional[str]]
    url_en: Mapped[Optional[str]]
    url_de: Mapped[Optional[str]]
    url_fr: Mapped[Optional[str]]
    url_api: Mapped[Optional[str]]
    request_id: Mapped[int] = mapped_column(ForeignKey("jobsch_requests.id"))
    sub_request_id: Mapped[int] = mapped_column(ForeignKey("jobsch_sub_requests.id"))

    date_log: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    sub_request = relationship("Sub_Request", back_populates="jobs")
    request = relationship("Request", back_populates="jobs")