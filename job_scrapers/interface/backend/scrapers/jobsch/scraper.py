from logging import Logger

from interface.backend.logger import logdef

from ..base import Scraper as BaseScraper

log: Logger = logdef(__name__)

BASE_API_JOB_URL: str = "https://www.jobs.ch/api/v1/public/search/job/"

BASE_API_JOB_URL_VAR: str = BASE_API_JOB_URL + "{job_id}"


class Scraper(BaseScraper):
    @classmethod
    def generate_sub_request_urls(cls, request_obj) -> list[str]:
        return [
            f"{request_obj.url_api}&page={x}" for x in range(1, request_obj.num_pages + 1)
        ]

    @classmethod
    async def extract_request_info(cls, rsp: dict):
        return dict(
            num_pages=rsp.get("data", {}).get("num_pages", ""),
            current_page=rsp.get("data", {}).get("current_page", ""),
            total_hits=rsp.get("data", {}).get("total_hits", ""),
            actual_hits=len(rsp.get("data", {}).get("documents", [])),
            norn_search_query=rsp.get("data", {}).get("normalized_search_query", ""),
            status=rsp.get("status"),
        )

    @classmethod
    async def extract_job_info(cls, job: dict):
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
            "url_en": job.get("_links").get("detail_de").get("href", ""),
            "url_de": job.get("_links").get("detail_fr").get("href", ""),
            "url_fr": job.get("_links").get("detail_en").get("href", ""),
            "url_api": BASE_API_JOB_URL_VAR.format(job_id=job.get("job_id", ""))
            # "links":job.get('_links', []),
        }

    @classmethod
    async def extract_job_full_info(cls, job: dict):
        return {
            "application_url": job.get("application_url", ""),
            "external_url": job.get("external_url", ""),
            "template": job.get("template", ""),
            "template_profession": job.get("template_profession", ""),
            "template_text": job.get("template_text", ""),
            "template_lead_text": job.get("template_lead_text", ""),
            "is_active": job.get("is_active", False),
            "is_paid": job.get("is_paid", False),
            "headhunter_application_allowed": job.get(
                "headhunter_application_allowed", False
            ),
            "publication_end_date": job.get("publication_end_date", ""),
            "contact_person": job.get("contact_person", ""),
            "status": job.get("status"),
        }

    @classmethod
    async def handle_Request(
        cls,
        request_obj,
        headers,
        cookies,
        request_dir="requests",
        site_name="jobsch",
    ):
        return await super().handle_request(
            request_obj,
            site_name,
            request_dir,
            cls.extract_request_info,
            headers,
            cookies,
        )

    @classmethod
    async def handle_sub_Request(
        cls,
        request_obj,
        headers,
        cookies,
    ):
        return await super().handle_sub_request(
            request_obj,
            "jobsch",
            cls.extract_request_info,
            headers,
            cookies,
        )

    @classmethod
    async def handle_Job(cls):
        pass