import asyncio
from logging import Logger
from typing import Optional

from interface.backend import db
from interface.backend import scrapers as scrp
from interface.backend.logger import logdef
from interface.backend.scrapers.base.scraper import BaseScraper

log: Logger = logdef(__name__)


async def mainEn(
    query,
    location,
    days,
    scraper,
    querybuilder,
    request_model,
    sub_request_model,
    job_model,
    job_id,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
):
    await db.init()

    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    request_obj: request_model = await db.create_record(
        request_model,
        query=query,
        location=location,
        days=days,
        url_api=querybuilder(query=query, location=location, days=days).url_api,
    )

    scpr = scraper(headers=headers, cookies=cookies)

    if request_data := await scpr.handle_request(request_obj):
        if sub_requests := await scpr.generate_sub_requests(
            request_obj, sub_request_model
        ):
            jobs = await scpr.handle_sub_requests(
                request_obj,
                sub_requests,
                job_model,
                job_id,
            )
            return jobs
        else:
            log.info("No sub_request were generated for %s", request_obj.url)
    else:
        log.info("No data found for url: %s", request_obj.url)


if __name__ == "__main__":
    for query in [
        # "Python",
        # "Software Developer",
        # "Data Science",
        # "Data Analysis",
        # "Data Analytics",
        # "Machine Learning",
        # "Web Development",
        # "Full Stack"
        "Software Engineering"
    ]:
        asyncio.run(
            mainEn(
                query=query,
                location="Switzerland",
                days=None,
                **scrp.jobsch.structure_dict,  # type: ignore
            )
        )
