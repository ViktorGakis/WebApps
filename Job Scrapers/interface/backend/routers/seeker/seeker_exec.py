from logging import Logger
from pprint import pformat

from job_seeker import seeker
from ...config import APISettings, get_api_settings
from ...logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


def seeker_arg_filter(rq_args: dict) -> dict[str, bool]:
    return dict(
        job_type=rq_args.get("job_type").strip().replace(" ", "").split(","),
        work_type=rq_args.get("work_type").strip().replace(" ", "").split(","),
        sort_by=rq_args.get("sort_by").strip().replace(" ", ""),
        posted=rq_args.get("posted").strip().replace(" ", ""),
        resume=bool(rq_args.get("resume").strip().replace(" ", "")),
    )


def seeker_exec(
    rq_args: dict,
    job_titles: list,
    not_words: list,
    locations: list,
    ip: str,
) -> str:
    exec_dict: dict[str, bool] = seeker_arg_filter(rq_args)
    log.info("exec_dict: \n%s", pformat(exec_dict))

    return seeker(
        job_titles=job_titles,
        not_words=not_words,
        locations=locations,
        job_types=exec_dict["job_type"],
        work_types=exec_dict["work_type"],
        sort_by=exec_dict["sort_by"],
        posted=exec_dict["posted"],
        resume=exec_dict["resume"],
        cookies=None,
        headers=None,
        ip=ip,
    )

