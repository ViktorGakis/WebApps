import asyncio
from logging import Logger

from interface.backend import scrapers as scrp
from interface.backend.logger import logdef

log: Logger = logdef(__name__)


if __name__ == "__main__":
    query_list = [
        {"query": "Python", "location": "Switzerland", "days": None},
        # {"query": "Software Engineering", "location": "Switzerland", "days": None},
        # {"query": "Software Developer", "location": "Switzerland", "days": None},
        # {"query": "Data Science", "location": "Switzerland", "days": None},
        # {"query": "Data Analysis", "location": "Switzerland", "days": None},
        # {"query": "Data Analytics", "location": "Switzerland", "days": None},
        {"query": "Machine Learning", "location": "Switzerland", "days": None},
        # {"query": "Web Development", "location": "Switzerland", "days": None},
        # {"query": "Full Stack", "location": "Switzerland", "days": None},
        # {"query": "Devops", "location": "Switzerland", "days": None},
        # {"query": "Programmer", "location": "Switzerland", "days": None},
    ]
    SCRPR = scrp.jobsch.Scraper({}, {})

    asyncio.run(
        SCRPR.main(
            query_list=query_list,
        )
    )
