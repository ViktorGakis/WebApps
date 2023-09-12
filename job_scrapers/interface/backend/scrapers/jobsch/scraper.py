from logging import Logger
from typing import Dict

from ... import db
from ...logger import logdef

# from interface.backend import db
# from interface.backend.logger import logdef
from ..base import BaseScraper
from . import QueryBuilder

log: Logger = logdef(__name__)

BASE_API_JOB_URL: str = "https://www.jobs.ch/api/v1/public/search/job/"

BASE_API_JOB_URL_VAR: str = BASE_API_JOB_URL + "{job_id}"


class Scraper(BaseScraper):
    def __init__(
        self, headers: Dict[str, str], cookies: Dict[str, str], site_name="jobsch"
    ) -> None:
        super().__init__(site_name, headers, cookies)

    def extract_request_info(self, rsp: dict):
        return dict(
            num_pages=rsp.get("data", {}).get("num_pages", ""),
            current_page=rsp.get("data", {}).get("current_page", ""),
            total_hits=rsp.get("data", {}).get("total_hits", ""),
            actual_hits=len(rsp.get("data", {}).get("documents", [])),
            norn_search_query=rsp.get("data", {}).get("normalized_search_query", ""),
            status=rsp.get("status"),
        )

    def generate_sub_request_urls(self, request_obj) -> list[str]:
        return [
            f"{request_obj.url_api}&page={x}"
            for x in range(1, request_obj.num_pages + 1)
        ]

    def extract_sub_request_info(self, rsp):
        return self.extract_request_info(rsp)

    def extract_job_info(self, job: dict):
        return {
            "title": job.get("title", ""),
            "publication_date": job.get("publication_date", ""),
            "company_name": job.get("company_name", ""),
            "place": job.get("place", ""),
            "is_active": job.get("is_active", False),
            "preview": job.get("preview", ""),
            "company_logo_file": job.get("company_logo_file", ""),
            "job_id": job.get("job_id", ""),
            "slug": job.get("slug", ""),
            "company_slug": job.get("company_slug", ""),
            "company_id": job.get("company_id", ""),
            "company_segmentation": job.get("company_segmentation", ""),
            "employment_position_ids": str(job.get("employment_position_ids", [])),
            "employment_grades": str(job.get("employment_grades", [])),
            "is_paid": job.get("is_paid", False),
            "work_experience": str(job.get("work_experience", [])),
            "language_skills": str(job.get("language_skills", [])),
            "url_en": job.get("_links").get("detail_en").get("href", ""),
            "url_de": job.get("_links").get("detail_de").get("href", ""),
            "url_fr": job.get("_links").get("detail_fr").get("href", ""),
            "url_api": BASE_API_JOB_URL_VAR.format(job_id=job.get("job_id", ""))
            # "links":job.get('_links', []),
        }

    def extract_job_request_info(self, job: dict):
        job_extr = job.get("data", {})
        return {
            "application_url": job_extr.get("application_url", ""),
            "external_url": job_extr.get("external_url", ""),
            "template": job_extr.get("template", ""),
            "template_profession": job_extr.get("template_profession", ""),
            "template_text": job_extr.get("template_text", ""),
            "template_lead_text": job_extr.get("template_lead_text", ""),
            "is_active": job_extr.get("is_active", False),
            "is_paid": job_extr.get("is_paid", False),
            "headhunter_application_allowed": job_extr.get(
                "headhunter_application_allowed", False
            ),
            "publication_end_date": job_extr.get("publication_end_date", ""),
            "contact_person": str(job_extr.get("contact_person", "")),
            "status": job.get("status"),
        }

    def extract_job_dict_from_sub_request(self, sub_request_data):
        return sub_request_data.get("data", {}).get("documents", [])

    async def get_uncompleted_jobs(self):
        conditions = [("status", "is", None), ("url_en", "not_is", None)]
        return await db.get_records(db.models.jobsch.Job, conditions, "and")

    async def main(self, query_list):
        return await super().main(
            query_list,
            querybuilder=QueryBuilder,
            request_model=db.models.jobsch.Request,
            sub_request_model=db.models.jobsch.Sub_Request,
            job_model=db.models.jobsch.Job,
            job_id="job_id",
        )
