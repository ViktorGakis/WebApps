import asyncio
import time
from logging import Logger
from typing import Optional

from interface.backend import db
from interface.backend import scrapers as scrp
from interface.backend.logger import logdef
from interface.backend.scrapers.base.scraper import BaseScraper

log: Logger = logdef(__name__)


if __name__ == "__main__":
    query_list = [
        {"query": "Python", "location": "Switzerland", "days": None},
        {"query": "Software Engineering", "location": "Switzerland", "days": None},
        # "Software Developer",
        # "Data Science",
        # "Data Analysis",
        # "Data Analytics",
        # "Machine Learning",
        # "Web Development",
        # "Full Stack"
    ]
    SCRPR = scrp.jobsch.Scraper({}, {})

    asyncio.run(
        SCRPR.main(
            query_list=query_list,
        )
    )
