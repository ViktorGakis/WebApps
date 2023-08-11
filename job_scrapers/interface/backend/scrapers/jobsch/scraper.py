from logging import Logger

from interface.backend.logger import logdef

from ..base import Scraper as BaseScraper

log: Logger = logdef(__name__)


class Scraper(BaseScraper):
    @classmethod
    def generate_sub_request_urls(cls, request_obj) -> list[str]:
        return [
            f"{request_obj.url}&page={x}" for x in range(1, request_obj.num_pages + 1)
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
            "is_active": job.get("is_active", ""),
            "preview": job.get("preview", ""),
            "company_logo_file": job.get("company_logo_file", ""),
            "job_id": job.get("job_id", ""),
            "slug": job.get("slug", ""),
            "company_slug": job.get("company_slug", ""),
            "company_id": job.get("company_id", ""),
            "company_segmentation": job.get("company_segmentation", ""),
            "employment_position_ids": str(job.get("employment_position_ids", [])),
            "employment_grades": str(job.get("employment_grades", [])),
            "is_paid": job.get("is_paid", ""),
            "work_experience": str(job.get("work_experience", [])),
            "language_skills": str(job.get("language_skills", [])),
            "job_url_en": job.get("_links").get("detail_de").get("href", ""),
            "job_url_de": job.get("_links").get("detail_fr").get("href", ""),
            "job_url_fr": job.get("_links").get("detail_en").get("href", "")
            # "links":job.get('_links', []),
        }



