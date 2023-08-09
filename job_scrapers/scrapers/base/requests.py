import asyncio
from logging import Logger
from typing import Any, Optional

import aiohttp

from interface.backend.logger import logdef

from .utils import write_to_file

log: Logger = logdef(__name__)


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



