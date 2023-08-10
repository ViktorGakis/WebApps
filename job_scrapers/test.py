import asyncio
from logging import Logger
from typing import Any, Optional

from interface.backend import db
from interface.backend.logger import logdef
from scrapers.base import Scraper
from scrapers.jobsdotch import QueryBuilder

log: Logger = logdef(__name__)


class Jobsch(Scraper):
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


async def mainEn(
    query="",
    location="",
    days="",
    querybuilder=QueryBuilder,
    request_dir: str = "jobsch",
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
):
    await db.init()

    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    request_url: str = querybuilder(query=query, location=location, days=days).url_api

    scraper = Jobsch()

    request_obj = await scraper.setup_request(
        db.models.Request,
        query=query,
        location=location,
        days=days,
        url=request_url,
    )

    request_data = await scraper.handle_request(
        [
            {
                "url": request_url,
                "headers": headers,
                "cookies": cookies,
                "request_obj": request_obj,
            },
            # Add more dictionaries for more URLs
        ],
        # may need to generalize for .html
        f"data/scraped/{request_dir}/requests/{request_obj.id}.json",
    )

    await scraper.handle_request_data(request_data, request_obj)

    if request_obj.num_pages > 0:
        sub_requests = await scraper.generate_sub_requests(
            request_obj, db.models.Sub_Request, scraper.generate_sub_request_urls
        )

        if sub_requests:
            await scraper.handle_sub_requests(
                headers, cookies, request_obj, sub_requests, request_dir, db.models.Job
            )
    else:
        log.info("No data found for url: %s", request_obj.url)


if __name__ == "__main__":
    print(
        asyncio.run(
            mainEn(
                "python",
                "Switzerland",
                "",
            )
        ),
    )
