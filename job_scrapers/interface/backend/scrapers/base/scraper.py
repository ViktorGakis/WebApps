import random
import time
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional

from interface.backend import db
from interface.backend.db.utils import check_attribute_exists
from interface.backend.logger import logdef

from .requests import fetch_all
from .utils import write_to_file

log: Logger = logdef(__name__)


class BaseScraper:
    CWD: Path = Path.cwd()
    NOT_IMPLEMENTED_MSG = "Needs to be defined in a subclass"

    def __init__(
        self, site_name: str, headers: Dict[str, str], cookies: Dict[str, str]
    ) -> None:
        self.SITE_NAME: str = site_name
        self.BASE_PATH: Path = self.CWD / Path(f"data/scraped/{self.SITE_NAME}")
        self.REQUEST_DIR: Path = self.BASE_PATH / Path("requests")
        self.SUBREQUEST_DIR: Path = self.BASE_PATH / Path("sub_requests")
        self.JOB_DIR: Path = self.BASE_PATH / Path("Jobs")
        self.HEADERS: Dict[str, str] = {} or headers
        self.COOKIES: Dict[str, str] = {} or cookies
        self.timeout_success: float = random.uniform(1, 1.5)
        self.timeout_failure: float = random.uniform(3, 4.5)

    async def handle_request_data(
        self, data_json, request_obj, request_dir, extract_request_info
    ) -> None:
        filepath: Path = request_dir / Path(f"{request_obj.id}.json")
        write_to_file(filepath, data_json.get("data", {}), "json")

        # log.info("data_json: \n%s", data_json)

        request_info: Dict[str, Any] = extract_request_info(data_json)

        # log.info("\request_obj: \n%s", request_obj)
        # log.info("\nrequest_info: \n%s", request_info)

        await db.update_record_from_dict([request_obj], [request_info])

        if request_info.get("status") == 200:
            time.sleep(self.timeout_success)
            # request_obj.logger(log, "info", " ")
            # request_obj.logger(log, "info", f" ({idx}/{len(jobs)})")
        elif request_info.get("status") != 404:
            time.sleep(self.timeout_failure)
            # request_obj.logger(log, "error", " ")
            # request_obj.logger(log, "error", f" ({idx}/{len(jobs)})")
        # request_obj.logger(log, "info", "")

    async def handle_abstr_request(
        self, url, request_obj, request_dir, extract_request_info
    ):
        req_data_dict: list[Any] = await fetch_all(
            [
                {
                    "url": url,
                    "headers": self.HEADERS,
                    "cookies": self.COOKIES,
                },
            ],
        )
        data_json = {}
        if data_json := req_data_dict[-1]:
            await self.handle_request_data(
                data_json, request_obj, request_dir, extract_request_info
            )
        else:
            log.info("Data for url: %s is empty", request_obj.url_api)
        return data_json

    async def handle_request(self, request_obj):
        return await self.handle_abstr_request(
            request_obj.url_api,
            request_obj,
            self.REQUEST_DIR,
            self.extract_request_info,
        )

    async def handle_sub_request(self, request_obj, sub_request_obj):
        return await self.handle_abstr_request(
            sub_request_obj.url_api,
            sub_request_obj,
            self.SUBREQUEST_DIR / Path(f"{request_obj.id}"),
            self.extract_sub_request_info,
        )

    async def handle_job_request(self, job):
        return await self.handle_abstr_request(
            job.url_api,
            job,
            self.JOB_DIR / Path(f"{job.request_id}") / Path(f"{job.sub_request_id}"),
            self.extract_job_request_info,
        )

    def extract_request_info(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    def generate_sub_request_urls(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    def extract_sub_request_info(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    def extract_job_info(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    def extract_job_dict_from_sub_request(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    def extract_job_request_info(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    async def get_uncompleted_jobs(self, *args, **kwds):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    def extract_job_dict_from_job_request(self):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MSG)

    async def generate_sub_requests(
        self,
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
            for url in self.generate_sub_request_urls(request_obj)
        ]
        await db.save_records(sub_requests)
        return sub_requests

    def handle_job(self, job_model, job_dict, request_obj, sub_request_obj):
        return job_model(
            **(self.extract_job_info(job_dict)),
            request_id=request_obj.id,
            sub_request_id=sub_request_obj.id,
        )

    async def handle_jobs(
        self, request_obj, sub_request_obj, sub_request_data, job_model, job_id: str
    ):
        jobs: list[job_model] = [
            self.handle_job(job_model, job_dict, request_obj, sub_request_obj)
            for job_dict in self.extract_job_dict_from_sub_request(sub_request_data)
        ]

        await self.handle_duplicate_jobs(
            request_obj, sub_request_obj, job_model, job_id, jobs
        )

        return jobs

    async def handle_duplicate_jobs(
        self, request_obj, sub_request_obj, job_model, job_id, jobs
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

    async def handle_sub_requests(
        self,
        request_obj,
        sub_requests,
        job_model,
        job_id,
    ):
        jobs = []
        for idx, sub_request in enumerate(sub_requests, start=1):
            if sub_request_data := await self.handle_sub_request(
                request_obj,
                sub_request,
            ):
                sub_request_info = self.extract_sub_request_info(sub_request_data)

                await db.update_record_from_dict([sub_request], [sub_request_info])

                jobs.append(
                    await self.handle_jobs(
                        request_obj, sub_request, sub_request_data, job_model, job_id
                    )
                )

                if sub_request_info.get("status") == 200:
                    time.sleep(self.timeout_success)
                    sub_request.logger(log, "info", f" ({idx}/{len(sub_requests)})")
                elif sub_request_info.get("status") != 404:
                    time.sleep(self.timeout_failure)
                    sub_request.logger(log, "error", f" ({idx}/{len(sub_requests)})")

        return jobs

    async def handle_job_requests(self):
        jobs = await self.get_uncompleted_jobs()
        for idx, job in enumerate(jobs, start=1):
            await self.handle_job_request(job)
            job.logger(log, "info", " ")
            

    async def main(
        self,
        query_list,
        querybuilder,
        request_model,
        sub_request_model,
        job_model,
        job_id,
    ):
        await db.init()

        for idx, query_dict in enumerate(query_list, start=1):
            query = query_dict["query"]
            location = query_dict["location"]
            days = query_dict["days"]

            request_obj: request_model = await db.create_record(
                request_model,
                query=query,
                location=location,
                days=days,
                url_api=querybuilder(query=query, location=location, days=days).url_api,
            )

            if request_data := await self.handle_request(request_obj):
                request_obj.logger(log, 'info', f' ({idx}/{len(query_list)})')
                if sub_requests := await self.generate_sub_requests(
                    request_obj, sub_request_model
                ):
                    jobs = await self.handle_sub_requests(
                        request_obj,
                        sub_requests,
                        job_model,
                        job_id,
                    )
                    await self.handle_job_requests()
                else:
                    log.info("No sub_request were generated for %s", request_obj.url)
                    if request_obj.status == 200:
                        time.sleep(1)
                    else:
                        time.sleep(3)
            else:
                log.info("No data found for url: %s", request_obj.url)
            
