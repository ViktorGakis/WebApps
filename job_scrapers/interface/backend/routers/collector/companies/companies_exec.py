from logging import Logger
from pprint import pformat
from typing import Optional

from pydantic import BaseModel, Extra, ValidationError, validator

from job_seeker import collector_companies
from job_seeker.collector.collector_companies_main import CollectorCompany

from ....config import APISettings, get_api_settings
from ....logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


class ExecArgs(BaseModel):
    """
    Collector_job exec vars API
    """

    chunk: Optional[int] = None
    change_headers: Optional[int] = 3
    resume: Optional[bool] = False
    repeats: Optional[int] = 1
    timeout: Optional[float] = 5
    timeout_req: Optional[float] = 1.5 

    class Config:
        extra: Extra = Extra.forbid

    @validator("*", pre=True)
    def chunk_val(cls, v, field):
        return field.default if (v == "" or v is None) else v


async def parse_exec_args(rq_args) -> ExecArgs | None:
    try:
        return ExecArgs.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())


def collector_companies_exec(
    rq_args: dict,
    ip: str,
) -> str:
    summary: str = ""
    try:
        exec_args: ExecArgs = ExecArgs.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())
    else:
        # try:
        log.info("\nexec_dict: \n%s", pformat(exec_args.dict()))
        summary = collector_companies(
            **exec_args.dict(),
            headers=None,
            cookies=None,
            ip=ip,
        )
        # except Exception as e:
        #     log.error("%s", e)

    return f"{summary}"
