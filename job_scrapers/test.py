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

    request_obj: request_model = await db.create_record(
        request_model,
        query=query,
        location=location,
        days=days,
        url_api=querybuilder(query=query, location=location, days=days).url_api,
    )

    if request_data := await scraper.handle_Request(request_obj, headers, cookies):
        if sub_requests := await scraper.generate_sub_requests(
            request_obj, sub_request_model
        ):
            for sub_request in sub_requests:
                if sub_request_data_json := await scraper.handle_sub_Request(
                    sub_request, headers, cookies
                ):
                    pass
                    # if sub_request_info:=scraper.extract:
                    #     pass

        else:
            log.info("No sub_request were generated for %s", request_obj.url)
    # await scraper.handle_request_data(request_data, request_obj)

    # if request_obj.num_pages > 0:
    #     sub_requests: list[sub_request_model] = await scraper.generate_sub_requests(
    #         request_obj, sub_request_model
    #     )

    #     if sub_requests:
    #         jobs = await scraper.handle_sub_requests(
    #             headers,
    #             cookies,
    #             request_obj,
    #             sub_requests,
    #             request_dir,
    #             job_model,
    #             job_id,
    #         )

    #         # print(f'{len(jobs[0])=}')

    #         await scraper.handle_jobs_full_info(
    #             jobs[0],
    #             request_dir,
    #             headers,
    #             cookies
    #         )

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
