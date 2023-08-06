import datetime
from datetime import datetime, timedelta
from pprint import pprint
from typing import Any, Dict, Optional
from urllib.parse import quote, quote_plus, urlencode

BASE_API_JOBS_URL: str = "https://www.jobs.ch/api/v1/public/search?"

BASE_URL: str = "https://www.jobs.ch/en/"
BASE_URL_JOBS: str = "https://www.jobs.ch/en/vacancies/?"

POSITION_TYPES_DICT: dict[str, Any] = {
    "api_field": "employment-position-ids%5B%5D",
    "domain_field": "position",
    "options": {"employee": "3", "specialist": "2", "executive position": "1"},
}


LANGUAGE_TYPES_DICT: dict[str, Any] = {
    "api_field": "language-skills%5B%5D",
    "domain_field": "language-skill",
    "options": {
        "english": "en",
        "french": "fr",
        "italian": "it",
        "german": "de",
        "not indicated": "missing",
    },
}


EMPLOYNMENT_TYPES_DICT: dict[str, Any] = {
    "api_field": "employment-type-ids%5B%5D",
    "domain_field": "employment-type",
    "options": {
        "apprenticeship": "6",
        "freelance": "2",
        "internship": "3",
        "supplementary income": "4",
        "temporary": "1",
        "unlimited employment": "5",
    },
}

COMPANY_SEGMENTS_DICT: dict[str, Any] = {
    "api_field": "company-segments%5B%5D",
    "domain_field": "segment",
    "options": {"small and medium": "kmu", "large": "gu", "consultants": "pdl"},
}


class QueryBuilder:
    def __init__(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        days: Optional[int] = None,
        work_load: Optional[list[int]] = None,
        position_types: Optional[list[str]] = None,
        languages: Optional[list[str]] = None,
        employment_types: Optional[list[str]] = None,
        company_types: Optional[list[str]] = None,
        page: int = 1,
    ) -> None:
        self.query: Optional[str] = query
        self.location: Optional[str] = location
        self.days: Optional[int] = days
        self.work_load: Optional[list[str]] = (
            [f"{x}" for x in work_load] if work_load else work_load
        )
        self.position_types: Optional[list[str]] = (
            [f"{x}" for x in position_types] if position_types else position_types
        )
        self.languages: Optional[list[str]] = (
            [f"{x}" for x in languages] if languages else languages
        )
        self.employment_types: Optional[list[str]] = (
            [f"{x}" for x in employment_types] if employment_types else employment_types
        )
        self.company_types: Optional[list[str]] = (
            [f"{x}" for x in company_types] if company_types else company_types
        )
        self.page: int = page
        self.current_api_url: Optional[str] = BASE_API_JOBS_URL
        self.current_url: Optional[str] = BASE_URL_JOBS
        self.params: dict[str, list] = {"api": [], "domain": []}
        self.gen_url()

    def gen_url(self) -> None:
        self.add_location()
        self.add_query()
        self.add_work_load()
        self.add_dates()
        self.add_positions()
        self.add_languages()
        self.add_employment_type()
        self.add_company_segments()
        self.add_page()
        self.build_urls()

    def add_location(self) -> None:
        if self.location:
            self.param_handle("location", self.location)

    def add_query(self) -> None:
        if self.query:
            self.param_handle("query", self.query, kind=["api"])
            self.param_handle("term", self.query, kind=["domain"])

    def add_work_load(self) -> None:
        if self.work_load and len(self.work_load) == 2:
            self.param_handle("employment-grade-max", str(self.work_load[-1]))
            self.param_handle("employment-grade-min", str(self.work_load[0]))

    def add_page(self):
        if self.page > 1:
            self.param_handle("page", str(self.page))

    def add_dates(self) -> None:
        if self.days:
            for k, v in self.generate_dates(self.days).items():
                self.param_handle(k, v, kind=["api"])
            self.param_handle("publication-date", str(self.days), kind=["domain"])

    def add_positions(self) -> None:
        if self.position_types:
            self.param_handle_dict(POSITION_TYPES_DICT, self.position_types)

    def add_languages(self) -> None:
        if self.languages:
            self.param_handle_dict(LANGUAGE_TYPES_DICT, self.languages)
            if 'not indicated' in self.languages:
                for i, tuple in enumerate(self.params['api']):
                    if tuple == ('language-skills%5B%5D', 'missing'):
                        self.params['api'][i] = ('language-skills%5B%5D', '')

    def add_employment_type(self) -> None:
        if self.employment_types:
            self.param_handle_dict(EMPLOYNMENT_TYPES_DICT, self.employment_types)

    def add_company_segments(self):
        if self.company_types:
            self.param_handle_dict(COMPANY_SEGMENTS_DICT, self.company_types)

    def param_handle(self, param, value, kind=None) -> None:
        if kind is None:
            kind: list[str] = ["api", "domain"]
        if "api" in kind:
            self.params["api"].append((param, value))
        if "domain" in kind:
            self.params["domain"].append((param, value))

    def param_handle_dict(self, info_dict: dict, key_list: list) -> None:
        for _, v in self.filter_dict_by_list(info_dict["options"], key_list).items():
            self.param_handle(info_dict["api_field"], v, ["api"])
            self.param_handle(info_dict["domain_field"], v, ["domain"])

    def build_urls(self) -> None:
        pprint(self.params)
        api_params: str = self.custom_urlencode(self.params["api"])
        domain_params: str = self.custom_urlencode(self.params["domain"])

        self.url_api: str = f"{BASE_API_JOBS_URL}{api_params}"
        self.url_domain: str = f"{BASE_URL_JOBS}{domain_params}"

    @staticmethod
    def custom_urlencode(query) -> str:
        return "&".join(
            f"{k}={v}" if "%20" in v else f"{k}={quote(str(v))}" for k, v in query
        )

    @staticmethod
    def filter_dict_by_list(dictionary, key_list):
        if not key_list:  # Check if the list is empty
            return {}
        return {key: dictionary[key] for key in key_list if key in dictionary}

    @staticmethod
    def generate_dates(days: int) -> Dict[str, Any]:
        # Get the current datetime
        now = datetime.now()

        # Subtract the number of days to get the "from" date, and set the time to 00:00:00
        from_date = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0)

        # Set the "to" datetime to the current day's end, i.e., 23:59:59
        to_date = now.replace(hour=23, minute=59, second=59)

        # Format the dates into strings
        from_str = quote(from_date.strftime("%Y-%m-%d %H:%M:%S"))
        to_str = quote(to_date.strftime("%Y-%m-%d %H:%M:%S"))

        return {
            "publication-date-from": from_str,
            "publication-date-to": to_str,
        }


# Ex# ample304: Provide all the optional arguments
query_builder = QueryBuilder(
    query="Software Engineer",
    location="Switzerland",
    days=1,
    work_load=[0, 100],
    position_types=["employee", "specialist"],
    languages=["english", "french", "italian", "german", "not indicated"],
    employment_types=[
        "apprenticeship",
        "freelance",
        "internship",
        "supplementary income",
        "temporary",
        "unlimited employment",
    ],
    company_types=["small and medium", "large", "consultants"],
)


print("----------------------------------------------------------------")
pprint(query_builder.params["api"])
print("----------------------------------------------------------------")
print(query_builder.url_api)
print("----------------------------------------------------------------")
pprint(query_builder.params["domain"])
print("----------------------------------------------------------------")
print(query_builder.url_domain)