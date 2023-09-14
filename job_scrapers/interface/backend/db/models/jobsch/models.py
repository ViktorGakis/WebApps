from collections import OrderedDict
from pprint import pformat
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Request(Base):
    __tablename__: str = "jobsch_requests"

    query: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    days: Mapped[Optional[int]]
    num_pages: Mapped[Optional[int]]
    total_hits: Mapped[Optional[int]]
    actual_hits: Mapped[Optional[int]]
    duplicates: Mapped[Optional[int]]
    current_page: Mapped[Optional[int]]
    url_api: Mapped[Optional[str]]

    sub_requests = relationship("Sub_Request", back_populates="request")
    jobs = relationship("Job", back_populates="request")
    status: Mapped[Optional[int]]

    def logger(self, logger, log_type, text):
        super().logger(
            logger,
            log_type,
            text,
            [
                "id",
                # "request_id",
                "status",
                "query",
                "location",
                "days",
                "current_page",
                "num_pages",
                "total_hits",
                "url_api",
            ],
        )


class Sub_Request(Base):
    __tablename__: str = "jobsch_sub_requests"

    query: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    days: Mapped[Optional[int]]
    num_pages: Mapped[Optional[int]]
    total_hits: Mapped[Optional[int]]
    actual_hits: Mapped[Optional[int]]
    duplicates: Mapped[Optional[int]]
    current_page: Mapped[Optional[int]]
    url_api: Mapped[Optional[str]]
    request_id: Mapped[int] = mapped_column(ForeignKey("jobsch_requests.id"))
    request = relationship("Request", back_populates="sub_requests")
    jobs = relationship("Job", back_populates="sub_request")
    status: Mapped[Optional[int]]

    def logger(self, logger, log_type, text):
        super().logger(
            logger,
            log_type,
            text,
            [
                "id",
                "request_id",
                "status",
                "query",
                "location",
                "days",
                "current_page",
                "num_pages",
                "total_hits",
                "url_api",
            ],
        )


class Job(Base):
    __tablename__: str = "jobsch_jobs"

    title: Mapped[Optional[str]]
    publication_date: Mapped[Optional[str]]
    publication_end_date: Mapped[Optional[str]]
    company_name: Mapped[Optional[str]]
    place: Mapped[Optional[str]]
    is_active: Mapped[Optional[bool]]
    job_id: Mapped[Optional[str]]
    preview: Mapped[Optional[str]]
    company_logo_file: Mapped[Optional[str]]
    slug: Mapped[Optional[str]]
    company_slug: Mapped[Optional[str]]
    company_id: Mapped[Optional[int]]
    company_segmentation: Mapped[Optional[str]]
    employment_position_ids: Mapped[Optional[str]]
    employment_grades: Mapped[Optional[str]]
    contact_person: Mapped[Optional[str]]
    is_paid: Mapped[Optional[bool]]
    work_experience: Mapped[Optional[str]]
    language_skills: Mapped[Optional[str]]
    url_en: Mapped[Optional[str]]
    url_de: Mapped[Optional[str]]
    url_fr: Mapped[Optional[str]]
    url_api: Mapped[Optional[str]]
    application_url: Mapped[Optional[str]]
    external_url: Mapped[Optional[str]]
    template: Mapped[Optional[str]]
    template_profession: Mapped[Optional[str]]
    template_text: Mapped[Optional[str]]
    template_lead_text: Mapped[Optional[str]]
    headhunter_application_allowed: Mapped[Optional[bool]]
    applied: Mapped[Optional[int]]
    saved: Mapped[Optional[int]]
    liked: Mapped[Optional[int]]
    expired: Mapped[Optional[int]]

    request_id: Mapped[int] = mapped_column(ForeignKey("jobsch_requests.id"))
    sub_request_id: Mapped[int] = mapped_column(ForeignKey("jobsch_sub_requests.id"))
    sub_request = relationship("Sub_Request", back_populates="jobs")
    request = relationship("Request", back_populates="jobs")
    status: Mapped[Optional[int]]

    def logger(self, logger, log_type, text) -> None:
        super().logger(
            logger,
            log_type,
            text,
            [
                "id",
                "request_id",
                "sub_request_id",
                "status",
                "title",
                "place",
                "company_name",
                # "num_pages",
                # "total_hits",
                # "url",
                "url_api",
            ],
        )
