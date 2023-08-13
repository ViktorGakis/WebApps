from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional

from interface.backend import db
from interface.backend.db.utils import check_attribute_exists
from interface.backend.logger import logdef

from .requests import fetch_all
from .utils import write_to_file

log: Logger = logdef(__name__)


class Request:
    @classmethod
    async def handle_request_data(
        cls, data_json, request_obj, site_name, request_dir, extract_request_info
    ):
        cwd: Path = Path.cwd()
        filepath: Path = cwd / Path(
            f"data/scraped/{site_name}/{request_dir}/{request_obj.id}.json"
        )

        write_to_file(filepath, data_json.get("data", {}), "json")

        request_info: Dict[str, Any] = await extract_request_info(data_json)

        await db.update_record_from_dict([request_obj], [request_info])

        request_obj.logger(log, "info", "")

    @classmethod
    async def handle_request(
        cls, request_obj, site_name, request_dir, extract_request_info, headers, cookies
    ):
        req_data_dict: list[Any] = await fetch_all(
            [
                {
                    "url": request_obj.url_api,
                    "headers": headers,
                    "cookies": cookies,
                },
            ],
        )
        data_json = {}
        if data_json := req_data_dict[-1]:
            await cls.handle_request_data(
                data_json, request_obj, site_name, request_dir, extract_request_info
            )
        else:
            log.info("Data for url: %s is empty", request_obj.url_api)
        return data_json


class SubRequest(Request):
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
        sub_requests: List[sub_request_model] = [
            sub_request_model(
                url_api=url,
                query=request_obj.query,
                location=request_obj.location,
                days=request_obj.days,
                request_id=request_obj.id,
            )
            for url in cls.generate_sub_request_urls(request_obj)
        ]
        await db.save_records(sub_requests)
        return sub_requests

    @classmethod
    async def handle_sub_request(
        cls, request_obj, site_name, extract_request_info, headers, cookies
    ):
        return await cls.handle_request(
            request_obj,
            site_name,
            "sub_requests",
            extract_request_info,
            headers,
            cookies,
        )

    @classmethod
    async def handle_sub_requests(
        cls, headers, cookies, request_obj, sub_requests, site_name, job_model, job_id
    ):
        jobs = []
        for idx, sub_request in enumerate(sub_requests, start=1):
            if sub_request_data := await cls.handle_sub_request(
                sub_request,
                site_name,
                "sub_requests",
                headers,
                cookies,
            ):
                # f"data/scraped/{request_dir}/sub_requests/{request_obj.id}/{sub_request.id}.json"
                sub_request_info = await cls.extract_request_info(sub_request_data)

                await cls.update_request_info(sub_request, sub_request_info)

            sub_request.logger(log, "info", f" ({idx}/{len(sub_requests)})")

            jobs.append(
                await cls.handle_jobs(
                    request_obj, sub_request, sub_request_data, job_model, job_id
                )
            )
        return jobs


class Scraper(SubRequest):
    pass


class JobUtils:
    pass


# class Scraper:
#     @classmethod
#     async def handle_jobs(
#         cls, request_obj, sub_request_obj, sub_request_data, job_model, job_id: str
#     ):
#         jobs: list[job_model] = [
#             job_model(
#                 **(await cls.extract_job_info(job_dict)),
#                 request_id=request_obj.id,
#                 sub_request_id=sub_request_obj.id,
#             )
#             for job_dict in sub_request_data.get("data", {}).get("documents", [])
#         ]

#         await cls.handle_duplicate_jobs(
#             request_obj, sub_request_obj, job_model, job_id, jobs
#         )

#         return jobs

#     @classmethod
#     async def handle_duplicate_jobs(
#         cls, request_obj, sub_request_obj, job_model, job_id, jobs
#     ):
#         jobs_unique: list[job_model] = []
#         jobs_dupl: list[job_model] = []
#         for job in jobs:
#             if await check_attribute_exists(
#                 job_model, job_id, value=getattr(job, job_id)
#             ):
#                 jobs_dupl.append(job)
#             else:
#                 jobs_unique.append(job)

#         async with db.async_session.begin() as ses:
#             ses.add_all(jobs_unique + [sub_request_obj, request_obj])

#             if sub_request_obj.duplicates is None and len(jobs_dupl):
#                 sub_request_obj.duplicates = 0 + len(jobs_dupl)
#             if request_obj.duplicates is None and len(jobs_dupl):
#                 request_obj.duplicates = 0 + len(jobs_dupl)

#     @classmethod
#     async def extract_request_info(cls, *args, **kwds):
#         raise NotImplementedError(
#             "extract_request_info needs to be defined in a subclass"
#         )

#     @classmethod
#     async def extract_job_info(cls, *args, **kwds):
#         raise NotImplementedError(
#             "extract_job_info_info needs to be defined in a subclass"
#         )

#     @classmethod
#     async def extract_job_full_info(cls, *args, **kwds):
#         raise NotImplementedError(
#             "extract_job_full_info needs to be defined in a subclass"
#         )

#     @classmethod
#     async def handle_request_job_full(cls, items, filepath):
#         data_json_list: list[Any] = await fetch_all(items)
#         if data_json := data_json_list[-1]:
#             write_to_file(filepath, data_json.get("data", {}), "json")
#             return data_json

#     @classmethod
#     async def handle_request_job_full_data(cls, request_data, request_obj):
#         if request_data.get("data", {}):
#             request_info = await cls.extract_job_full_info(request_data)

#             await cls.update_request_info(request_obj, request_info)

#             request_obj.logger(log, "info", "")

#     @classmethod
#     async def handle_job_full_info(
#         cls,
#         job,
#         request_dir,
#         headers,
#         cookies,
#     ):
#         job_data = await cls.handle_request_job_full(
#             [
#                 {
#                     "url": job.url_api,
#                     "headers": headers,
#                     "cookies": cookies,
#                 },
#             ],
#             f"data/scraped/{request_dir}/jobs/{job.id}.json",
#         )

#         print("--------------------------")
#         print(f"{job_data=}")
#         print("--------------------------")
#         job_info = await cls.extract_job_full_info(job_data.get("data", {}))

#         await cls.update_request_info(job, job_info)
#         return job_info

#     @classmethod
#     async def handle_jobs_full_info(
#         cls,
#         jobs,
#         request_dir,
#         headers,
#         cookies,
#     ):
#         for idx, job in enumerate(jobs, start=1):
#             print("--------------------------")
#             print(f"{job=}")
#             print("--------------------------")
#             job_info = await cls.handle_job_full_info(
#                 job,
#                 request_dir,
#                 headers,
#                 cookies,
#             )
#             print("--------------------------")
#             print(f"{job_info=}")
#             print("--------------------------")
#             # job.logger(log, "info", f" ({idx}/{len(jobs)})")
#             break
