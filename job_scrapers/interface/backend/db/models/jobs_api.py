from typing import Any

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from ..base import Base


class Job_Api(Base):
    __tablename__: str = "jobs_api"
    id = Column("id", Integer(), primary_key=True)
    title = Column("title", String)
    publication_date = Column("publication_date", String)
    company_name = Column("company_name", String, default=None)
    place = Column("place", String, default=None)
    is_active = Column("is_active", Boolean)
    preview = Column("preview", String, default=None)
    company_logo_file = Column("company_logo_file", String, default=None)
    job_id = Column("job_id", String, default=None)
    slug = Column("slug", String, default=None)
    company_slug = Column("company_slug", String, default=None)
    company_id = Column("company_id", Integer, default=None)
    company_segmentation = Column("company_segmentation", String, default=None)
    employment_position_ids = Column("employment_position_ids", String, default=None)
    employment_grades = Column("employment_grades", String, default=None)
    is_paid = Column("is_paid", Boolean)
    work_experience = Column("work_experience", String, default=None)
    language_skills = Column("language_skills", String, default=None)

    job_url_en = Column("job_url_en", String, default=None)
    job_url_de = Column("job_url_de", String, default=None)
    job_url_fr = Column("job_url_fr", String, default=None)

    query_id = Column("query_id", Integer, default=None)
    subquery_id = Column("subquery_id", Integer, default=None)
    dateLog = Column(
        "dateLog", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def __init__(
        self,
        title: String,
        publication_date: String,
        company_name: String,
        place: String,
        is_active: Boolean,
        preview: String,
        company_logo_file: String,
        job_id: String,
        slug: String,
        company_slug: String,
        company_id: String,
        company_segmentation: String,
        employment_position_ids: String,
        employment_grades: String,
        is_paid: Boolean,
        work_experience: String,
        language_skills: String,
        job_url_en: String,
        job_url_de: String,
        job_url_fr: String,
        query_id: Integer = query_id,
        subquery_id: Integer = subquery_id,
    ) -> None:
        self.title: String = title
        self.publication_date: String = publication_date
        self.company_name: String = company_name
        self.place: String = place
        self.is_active: Boolean = is_active
        self.preview: String = preview
        self.company_logo_file: String = company_logo_file
        self.job_id: String = job_id
        self.slug: String = slug
        self.company_slug: String = company_slug
        self.company_id: String = company_id
        self.company_segmentation: String = company_segmentation
        self.employment_position_ids: String = employment_position_ids
        self.employment_grades: String = employment_grades
        self.is_paid: Boolean = is_paid
        self.work_experience: String = work_experience
        self.language_skills: String = language_skills
        self.job_url_en: String = job_url_en
        self.job_url_de: String = job_url_de
        self.job_url_fr: String = job_url_fr
        self.query_id: Integer = query_id
        self.subquery_id: Integer = subquery_id

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "publication_date": self.publication_date,
            "company_name": self.company_name,
            "place": self.place,
            "is_active": self.is_active,
            "preview": self.preview,
            "company_logo_file": self.company_logo_file,
            "job_id": self.job_id,
            "slug": self.slug,
            "company_slug": self.company_slug,
            "company_id": self.company_id,
            "company_segmentation": self.company_segmentation,
            "employment_position_ids": self.employment_position_ids,
            "employment_grades": self.employment_grades,
            "is_paid": self.is_paid,
            "work_experience": self.work_experience,
            "language_skills": self.language_skills,
            "job_url_en": self.job_url_en,
            "job_url_de": self.job_url_de,
            "job_url_fr": self.job_url_fr,
            "query_id": self.query_id,
            "subquery_id": self.subquery_id,
            "dateLog": self.dateLog,
        }

    def __repr__(self) -> str:
        return f"{self.serialize()}"
