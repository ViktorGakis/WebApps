from logging import Logger
from typing import Any

from interface.backend import db
from interface.backend.db.utils import check_attribute_exists
from interface.backend.logger import logdef

from .requests import fetch_all
from .utils import write_to_file

log: Logger = logdef(__name__)


class Scraper:
    @classmethod
    async def setup_request(cls, RequestModel, *args, **kwds):
        async with db.async_session.begin() as ses:
            req = RequestModel(*args, **kwds)
            ses.add_all([req])
            await ses.commit()
            return req

    @classmethod
    async def update_request_info(cls, request_obj, request_info):
        for k, v in request_info.items():
            setattr(request_obj, k, v)

        async with db.async_session.begin() as ses:
            ses.add_all([request_obj])
            await ses.commit()

    @classmethod
    async def handle_request(cls, items, filepath):
        data_json_list: list[Any] = await fetch_all(items)
        if data_json := data_json_list[-1]:
            write_to_file(filepath, data_json.get("data", {}), "json")
            return data_json

    @classmethod
    async def handle_request_data(cls, request_data, request_obj):
        if request_data.get("data", {}):
            request_info = await cls.extract_request_info(request_data)

            await cls.update_request_info(request_obj, request_info)
            
            

    @classmethod
    async def extract_request_info(cls, *args, **kwds):
        raise NotImplementedError(
            "extract_request_info needs to be defined in a subclass"
        )

    @classmethod
    async def extract_job_info(cls, *args, **kwds):
        raise NotImplementedError(
            "extract_job_info_info needs to be defined in a subclass"
        )

    @classmethod
    async def extract_job_info_full(cls, *args, **kwds):
        raise NotImplementedError(
            "extract_job_info_full needs to be defined in a subclass"
        )

    @classmethod
    def generate_sub_request_urls(cls, *args, **kwds):
        raise NotImplementedError(
            "generate_sub_request_urls needs to be defined in a subclass"
        )

    @classmethod
    async def generate_sub_requests(
        cls,
        request_obj,
        sub_request_model,
    ):
        sub_requests = [
            sub_request_model(
                url=url,
                query=request_obj.query,
                location=request_obj.location,
                days=request_obj.days,
                request_id=request_obj.id,
            )
            for url in cls.generate_sub_request_urls(request_obj)
        ]
        async with db.async_session.begin() as ses:
            ses.add_all(sub_requests)
            await ses.commit()
        return sub_requests

    @classmethod
    async def handle_sub_requests(
        cls, headers, cookies, request_obj, sub_requests, request_dir, job_model, job_id
    ):
        for sub_request in sub_requests:
            if sub_request_data := await cls.handle_request(
                [
                    {
                        "url": sub_request.url,
                        "headers": headers,
                        "cookies": cookies,
                    },
                    # Add more dictionaries for more URLs
                ],
                # may need to generalize for .html files
                f"data/scraped/{request_dir}/sub_requests/{request_obj.id}/{sub_request.id}.json",
            ):
                sub_request_info = await cls.extract_request_info(sub_request_data)

                await cls.update_request_info(sub_request, sub_request_info)
                
                # async with db.async_session.begin() as ses:
                #     ses.add(sub_request)
                #     await ses.commit()
                #     log.info("%s", f"{sub_request}")

                return await cls.handle_jobs(
                    request_obj, sub_request, sub_request_data, job_model, job_id
                )

    @classmethod
    async def handle_jobs(
        cls, request_obj, sub_request_obj, sub_request_data, job_model, job_id: str
    ):
        jobs: list[job_model] = [
            job_model(
                **(await cls.extract_job_info(job_dict)),
                request_id=request_obj.id,
                sub_request_id=sub_request_obj.id,
            )
            for job_dict in sub_request_data.get("data", {}).get("documents", [])
        ]

        await cls.handle_duplicate_jobs(
            request_obj, sub_request_obj, job_model, job_id, jobs
        )

        return jobs

    @classmethod
    async def handle_duplicate_jobs(
        cls, request_obj, sub_request_obj, job_model, job_id, jobs
    ):
        jobs_unique: list[job_model] = []
        jobs_dupl: list[job_model] = []
        for job in jobs:
            if await check_attribute_exists(
                job_model, job_id, value=getattr(job, job_id)
            ):
                jobs_dupl.append(job)
            else:
                jobs_unique.append(job)

        async with db.async_session.begin() as ses:
            ses.add_all(jobs_unique + [sub_request_obj, request_obj])

            if sub_request_obj.duplicates is None and len(jobs_dupl):
                sub_request_obj.duplicates = 0 + len(jobs_dupl)
            if request_obj.duplicates is None and len(jobs_dupl):
                request_obj.duplicates = 0 + len(jobs_dupl)
