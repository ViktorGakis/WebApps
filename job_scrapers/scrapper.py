from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
import asyncio
import json
from pathlib import Path
from typing import Any, Optional, Union

import aiohttp
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from interface.backend import db
from scrapers.jobsdotch import QueryBuilder


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

        print(f"Successfully wrote the data to '{filepath}' in {data_format} format.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
            content_type = response.headers.get("Content-Type", "")
            # print(f"{content_type=}")
            if "application/json" in content_type:
                # If it's JSON, use .json() method
                return dict(data=await response.json(), status=response.status)
            else:
                # Otherwise, return as text
                return dict(data=await response.text(), status=response.status)
        print(f"Failed to fetch {url}. Status: {response.status}")
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
                print(f"Failed to fetch {url} after {retries} attempts. Error: {e}")
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
    data_json_list = await fetch_all(items)
    if data_json := data_json_list[0]:
        write_to_file(filepath, data_json.get("data", {}), "json")
        return data_json


async def create_query(query, location, days, url, model):
    return (
        await db.create_objs(
            model,
            [dict(query=query, location=location, days=days, url=url)],
        )
    )[0][0]


def generate_subqueries_urls(base_url, numPages) -> list[str]:
    return [f"{base_url}&page={x}" for x in range(1, numPages + 1)]


async def generate_subqueries(
    num_pages, queryPrimaryKey, query, location, days, model_retrieve, model_create
):
    base_url = (await db.retrieve_objs([queryPrimaryKey], model_retrieve))[0].url
    if num_pages > 1:
        urls: list[str] = generate_subqueries_urls(base_url, num_pages)
        spkeys: list[Any] = await db.create_objs(
            model_create,
            [
                dict(
                    url=url,
                    qpkey=queryPrimaryKey,
                    query=query,
                    location=location,
                    days=days,
                    page=page,
                )
                for page, url in enumerate(urls, start=1)
            ],
        )
        return [x[0] if isinstance(x, tuple) else x for x in spkeys]
    else:
        return [x[0] if isinstance(x, tuple) else x for x in [queryPrimaryKey]]


async def extract_query_info(rsp: dict):
    return dict(
        num_pages=rsp.get("data", {}).get("num_pages", ""),
        current_page=rsp.get("data", {}).get("current_page", ""),
        total_hits=rsp.get("data", {}).get("total_hits", ""),
        actual_hits=len(rsp.get("data", {}).get("documents", [])),
        status=rsp.get("status", None),
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
    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    await db.init()

    async with db.async_session.begin() as ses:
        req = db.models.Request(
            url=QueryBuilder(query=query, location=location, days=days).url_api
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
            # sub_reqs = []
            query_info = await extract_query_info(req_data_json)

            for k, v in query_info.items():
                setattr(req, k, v)

            async with db.async_session.begin() as ses:
                ses.add_all([req])
                await ses.commit()

            if req.num_pages > 1:
                if sub_reqs := [
                    db.models.SubRequest(url=url)
                    for url in generate_subqueries_urls(req.url, req.num_pages)
                ]:
                    async with db.async_session.begin() as ses:
                        ses.add_all([req, *sub_reqs])
                        await ses.commit()

            if sub_reqs:
                for sub_req in sub_reqs:
                    if sub_req_data_json := await handle_request(
                        [
                            {
                                "url": sub_req.url,
                                "name": "",
                                "headers": headers,
                                "cookies": cookies,
                            },
                            # Add more dictionaries for more URLs
                        ],
                        f"data/json/jobsch/sub_requests/{req.id}/{sub_req.id}.json",
                    ):
                        sub_req_info = await extract_query_info(sub_req_data_json)

                        for k, v in sub_req_info.items():
                            setattr(sub_req, k, v)

                        async with db.async_session.begin() as ses:
                            ses.add_all(sub_reqs)



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
