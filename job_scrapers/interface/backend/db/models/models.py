from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..base import Base


class Request(Base):
    __tablename__: str = "requests"
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


class SubRequest(Base):
    __tablename__: str = "subrequests"
    # __table_args__: tuple[dict[str, bool]] = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Optional[int]]
    query: Mapped[Optional[str]] = mapped_column(ForeignKey("requests.query"))
    location: Mapped[Optional[str]] = mapped_column(ForeignKey("requests.location"))
    days: Mapped[Optional[int]] = mapped_column(ForeignKey("requests.days"))
    num_pages: Mapped[Optional[int]]
    total_hits: Mapped[Optional[int]]
    actual_hits: Mapped[Optional[int]]
    duplicates: Mapped[Optional[int]]
    current_page: Mapped[Optional[int]]
    url: Mapped[Optional[str]]
    query_id: Mapped[Optional[int]] = mapped_column(ForeignKey("requests.id"))
    date_log: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class Job(Base):
    __tablename__: str = "jobs"
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
    job_url_en: Mapped[Optional[str]]
    job_url_de: Mapped[Optional[str]]
    job_url_fr: Mapped[Optional[str]]
    query_id: Mapped[Optional[int]] = mapped_column(ForeignKey("requests.id"))
    subquery_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subrequests.id"))
    date_log: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
