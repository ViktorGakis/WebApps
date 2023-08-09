import asyncio
import json
from logging import Logger
from pathlib import Path
from typing import Any, Optional, Union

import aiohttp
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from IPython.core.interactiveshell import InteractiveShell
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from interface.backend import db
from scrapers.jobsdotch import QueryBuilder

from interface.backend.logger import logdef

InteractiveShell.ast_node_interactivity = "all"

log: Logger = logdef(__name__)

def read_from_file(filepath: Path, parser: str) -> BeautifulSoup:
    with filepath.open(mode="r", encoding="utf-8") as file:
        return BeautifulSoup(file.read(), features=parser)


def write_to_file(filepath: Path, data: Union[str, dict], data_format: str = "text"):
    try:
        # Create a Path object from the provided file path
        path = Path(filepath)

        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        if data_format == "text":
            # If data is BeautifulSoup, convert it to a prettified string
            if isinstance(data, BeautifulSoup):
                data = str(data.prettify())

            # Write the content to the file as text
            with path.open(mode="w", encoding="utf-8") as file:
                file.write(data)
        elif data_format == "json":
            # If data is a dictionary, convert it to a JSON-formatted string
            if isinstance(data, dict):
                data = json.dumps(data, indent=4)

            # Write the JSON content to the file
            with path.open(mode="w", encoding="utf-8") as file:
                file.write(data)
        else:
            raise ValueError("Invalid data format. Use 'text' or 'json'.")

        log.info(f"Successfully wrote the data to '{filepath}' in {data_format} format.")
    except Exception as e:
        log.error(f"An error occurred: {e}")


def soup(
    source: Union[
        BeautifulSoup, NavigableString, ResultSet, Tag, WebElement, WebDriver, str, Path
    ],
    parser="html.parser",
    filepath: Optional[Path | str] = "temp.html",
) -> BeautifulSoup:
    soupen = None

    if isinstance(source, (BeautifulSoup, NavigableString, ResultSet, Tag)):
        soupen = source
    elif isinstance(source, Path) and source.exists():
        soupen = read_from_file(source, parser)
    elif isinstance(source, str):
        path = Path(source)
        if path.exists():
            soupen = read_from_file(path, parser)
        else:
            soupen = BeautifulSoup(source, features=parser)
    elif isinstance(source, WebElement):
        source_html: str = source.get_attribute("innerHTML")
        soupen = BeautifulSoup(source_html, features=parser)
    elif isinstance(source, WebDriver):
        source_html: str = source.page_source
        soupen = BeautifulSoup(source_html, features=parser)

    if filepath and soupen is not None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_to_file(path, soupen)

    return soupen


async def _make_request(
    session: aiohttp.ClientSession,
    url: str,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
) -> Any:
    async with session.get(url, headers=headers, cookies=cookies) as response:
        if response.status == 200:
            # Check the content type of the response
            content_type: str = response.headers.get("Content-Type", "")
            # print(f"{content_type=}")
            if "application/json" in content_type:
                # If it's JSON, use .json() method
                return dict(data=await response.json(), status=response.status)
            else:
                # Otherwise, return as text
                return dict(data=await response.text(), status=response.status)
        log.error(f"Failed to fetch {url}. Status: {response.status}")
        return None


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    retries=3,
    timeout_for_wait: Optional[float] = None,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
) -> Any:
    for i in range(retries):
        try:
            return await asyncio.wait_for(
                _make_request(session, url, headers, cookies),
                timeout=timeout_for_wait,
            )
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if i == retries - 1:  # This was the last attempt
                log.error(f"Failed to fetch {url} after {retries} attempts. Error: {e}")
                return None


async def fetch_all(items, retries=3, timeout_for_session=5) -> list:
    timeout = aiohttp.ClientTimeout(total=timeout_for_session)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            fetch(
                session,
                item["url"],
                retries,
                timeout_for_session,
                item.get("headers"),
                item.get("cookies"),
            )
            for item in items
        ]
        return await asyncio.gather(*tasks)


#########################################################


async def handle_request(items, filepath):
    data_json_list: list[Any] = await fetch_all(items)
    if data_json := data_json_list[0]:
        write_to_file(filepath, data_json.get("data", {}), "json")
        return data_json


def generate_subqueries_urls(base_url, numPages) -> list[str]:
    return [f"{base_url}&page={x}" for x in range(1, numPages + 1)]


async def extract_query_info(rsp: dict):
    return dict(
        num_pages=rsp.get("data", {}).get("num_pages", ""),
        current_page=rsp.get("data", {}).get("current_page", ""),
        total_hits=rsp.get("data", {}).get("total_hits", ""),
        actual_hits=len(rsp.get("data", {}).get("documents", [])),
        norn_search_query= rsp.get('data', {}).get('normalized_search_query',""),
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


async def mainEn(
    query="",
    location="",
    days="",
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
):

    await db.init()

    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}


    async with db.async_session.begin() as ses:
        req = db.models.Request(
            query=query,
            location=location,
            days=days,
            url=QueryBuilder(query=query, location=location, days=days).url_api,
        )
        ses.add_all([req])
        await ses.commit()

    if req_data_json := await handle_request(
        [
            {
                "url": req.url,
                "name": "",
                "headers": headers,
                "cookies": cookies,
            },
            # Add more dictionaries for more URLs
        ],
        f"data/json/jobsch/requests/{req.id}.json",
    ):
        if req_data_json.get("data", {}):
            sub_reqs = []
            query_info = await extract_query_info(req_data_json)

            for k, v in query_info.items():
                setattr(req, k, v)

            async with db.async_session.begin() as ses:
                ses.add_all([req])
                await ses.commit()

            if req.num_pages > 1:
                if sub_reqs := [
                    db.models.Sub_Request(
                        url=url,
                        query=req.query,
                        location=req.location,
                        days=req.days,
                        request_id=req.id,
                    )
                    for url in generate_subqueries_urls(req.url, req.num_pages)
                ]:
                    async with db.async_session.begin() as ses:
                        ses.add_all([req, *sub_reqs])
                        await ses.commit()

            if sub_reqs:
                for sub_request in sub_reqs:
                    if sub_req_data_json := await handle_request(
                        [
                            {
                                "url": sub_request.url,
                                "name": "",
                                "headers": headers,
                                "cookies": cookies,
                            },
                            # Add more dictionaries for more URLs
                        ],
                        f"data/json/jobsch/sub_requests/{req.id}/{sub_request.id}.json",
                    ):
                        sub_req_info = await extract_query_info(sub_req_data_json)

                        for k, v in sub_req_info.items():
                            setattr(sub_request, k, v)

                        async with db.async_session.begin() as ses:
                            ses.add_all([sub_request])
                            await ses.commit()

                        # print(f'{sub_req_data_json=}')

                        jobs: list[db.models.Job] = [
                            db.models.Job(
                                **(await extract_job_info(job_dict)),
                                request_id=req.id,
                                sub_request_id=sub_request.id,
                            )
                            for job_dict in sub_req_data_json.get("data", {}).get(
                                "documents", []
                            )
                        ]

                        async with db.async_session.begin() as ses:
                            ses.add_all(jobs)
                            await ses.commit()


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
