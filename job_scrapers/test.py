import asyncio
from logging import Logger
from typing import Optional

from interface.backend import db
from interface.backend import scrapers as scrp
from interface.backend.logger import logdef

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
    request_dir: str,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
):
    await db.init()

    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    request_url: str = querybuilder(query=query, location=location, days=days).url_api

    request_obj = await scraper.setup_request(
        request_model,
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
        sub_requests: list[sub_request_model] = await scraper.generate_sub_requests(
            request_obj, sub_request_model, scraper.generate_sub_request_urls
        )

        if sub_requests:
            await scraper.handle_sub_requests(
                headers,
                cookies,
                request_obj,
                sub_requests,
                request_dir,
                job_model,
                job_id,
            )
    else:
        log.info("No data found for url: %s", request_obj.url)


if __name__ == "__main__":
    for query in [
        "Python",
        "Software Developer",
        "Data Science",
        "Data Analysis",
        "Data Analytics",
        "Machine Learning",
        "Web Development",
    ]:
        asyncio.run(
            mainEn(
                query=query,
                location="Switzerland",
                days=None,
                **scrp.jobsch.structure_dict,  # type: ignore
            )
        )
