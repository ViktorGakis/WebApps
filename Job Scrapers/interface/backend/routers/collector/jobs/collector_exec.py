from logging import Logger
from pprint import pformat
from typing import Optional

from pydantic import BaseModel, Extra, ValidationError, validator

from job_seeker import collector_jobs

from ....config import APISettings, get_api_settings
from ....logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


class ExecArgs(BaseModel):
    """
    Collector_job exec vars API
    """

    chunk: Optional[int] = None
    sleep_min: Optional[int] = 1
    sleep_max: Optional[int] = 3
    resume: Optional[str] = None

    class Config:
        extra: Extra = Extra.forbid

    @validator("chunk", "sleep_min", "sleep_max", pre=True)
    def chunk_val(cls, v, field):
        return field.default if (v == "" or v is None) else v

    @validator("resume", pre=True)
    def resume_val(cls, v, field):
        return v if v in ["Not 200", "No content", "All"] else field.default


def collector_exec(
    rq_args: dict,
    ip: str,
) -> str:
    summary: str = ""
    try:
        exec_args: ExecArgs = ExecArgs.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())
    else:
        try:
            log.info("exec_dict: \n%s", pformat(exec_args.dict()))
            summary = collector_jobs(
                **exec_args.dict(),
                cookies=None,
                headers=None,
                ip=ip,
            )
        except Exception as e:
            log.error("%s", e)

    return f"{summary}"
