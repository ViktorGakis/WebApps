import asyncio
from logging import Logger
from typing import Any, Optional

from interface.backend import db
from interface.backend.logger import logdef

from ..jobsdotch import QueryBuilder
from .requests import fetch_all
from .utils import write_to_file

log: Logger = logdef(__name__)


class Scraper:
    async def setup_request(self, *args, **kwds):
        pass
    
    async def update_request_info(self, *args, **kwds):
        pass

    async def handle_request(self, *args, **kwds):
        pass
    
    async def handle_request_data(self, *args, **kwds):
        pass

    async def extract_request_info(self, *args, **kwds):
        pass

    async def extract_job_info(self, *args, **kwds):
        pass

    def generate_sub_request_urls(self, *args, **kwds):
        pass
    
    async def generate_sub_requests(self, *args, **kwds):
        pass
    
    async def handle_sub_requests(self, *args, **kwds):
        pass
    
    async def handle_jobs(self, *args, **kwds):
        pass


def generate_sub_request_urls(base_url, numPages) -> list[str]:
    return [f"{base_url}&page={x}" for x in range(1, numPages + 1)]


async def extract_request_info(rsp: dict):
    return dict(
        num_pages=rsp.get("data", {}).get("num_pages", ""),
        current_page=rsp.get("data", {}).get("current_page", ""),
        total_hits=rsp.get("data", {}).get("total_hits", ""),
        actual_hits=len(rsp.get("data", {}).get("documents", [])),
        norn_search_query=rsp.get("data", {}).get("normalized_search_query", ""),
        status=rsp.get("status"),
    )


async def extract_job_info(job: dict):
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


async def setup_request(RequestModel, *args, **kwds):
    async with db.async_session.begin() as ses:
        req = RequestModel(*args, **kwds)
        ses.add_all([req])
        await ses.commit()
        return req


async def update_request_info(request_obj, request_info):
    for k, v in request_info.items():
        setattr(request_obj, k, v)

    async with db.async_session.begin() as ses:
        ses.add_all([request_obj])
        await ses.commit()


async def handle_request(items, filepath):
    data_json_list: list[Any] = await fetch_all(items)
    if data_json := data_json_list[-1]:
        write_to_file(filepath, data_json.get("data", {}), "json")
        return data_json


async def handle_request_data(request_data, request_obj):
    if request_data.get("data", {}):
        request_info = await extract_request_info(request_data)

        await update_request_info(request_obj, request_info)


async def generate_sub_requests(
    request_obj, sub_request_model=None, generate_sub_request_urls=None
):
    if sub_request_model is not None and generate_sub_request_urls is not None:
        sub_requests = [
            sub_request_model(
                url=url,
                query=request_obj.query,
                location=request_obj.location,
                days=request_obj.days,
                request_id=request_obj.id,
            )
            for url in generate_sub_request_urls(request_obj)
        ]
        async with db.async_session.begin() as ses:
            ses.add_all(sub_requests)
            await ses.commit()
        return sub_requests
    return


async def handle_sub_requests(
    headers, cookies, request_obj, sub_requests, request_dir, job_model
):
    for sub_request in sub_requests:
        if sub_request_data := await handle_request(
            [
                {
                    "url": sub_request.url,
                    "headers": headers,
                    "cookies": cookies,
                },
                # Add more dictionaries for more URLs
            ],
            # may need to generalize for .html files
            f"data/{request_dir}/sub_requests/{request_obj.id}/{sub_request.id}.json",
        ):
            sub_request_info = await extract_request_info(sub_request_data)

            await update_request_info(sub_request, sub_request_info)

            await handle_jobs(request_obj, sub_request, sub_request_data, job_model)


async def handle_jobs(request_obj, sub_request, sub_request_data, job_model):
    jobs: list[job_model] = [
        job_model(
            **(await extract_job_info(job_dict)),
            request_id=request_obj.id,
            sub_request_id=sub_request.id,
        )
        for job_dict in sub_request_data.get("data", {}).get("documents", [])
    ]

    async with db.async_session.begin() as ses:
        ses.add_all(jobs)


async def mainEn(
    query="",
    location="",
    days="",
    querybuilder = QueryBuilder,
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

    request_obj = await setup_request(
        query, location, days, request_url, db.models.Request
    )

    request_data = await handle_request(
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

    await handle_request_data(request_data, request_obj)

    if request_obj.num_pages > 1:
        sub_requests = await generate_sub_requests(
            request_obj, db.models.Sub_Request, generate_sub_request_urls
        )

        if sub_requests:
            await handle_sub_requests(
                headers, cookies, request_obj, sub_requests, request_dir, db.models.Job
            )
    else:
        log.info("No data found for url: %", request_obj.url)


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
