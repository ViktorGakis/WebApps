from collections import OrderedDict
import json
from logging import Logger
from typing import Optional

from fastapi.responses import JSONResponse
from pandas import DataFrame
from plotly.graph_objects import Figure
from pydantic import BaseModel, Extra, ValidationError, validator

from job_seeker import (
    ExpiredChecker_args,
    generate_map,
)
from job_seeker.db import load_df
from job_seeker.final_filters.analytics import Analytics

from ...logger import logdef
from ..utils import (
    exec_block,
    jsonResp,
    jsonify_plotly,
)

log: Logger = logdef(__name__)


class ExecArgs(BaseModel):
    """
    Collector_job exec vars API
    """

    days_ago_min: Optional[int] = ExpiredChecker_args["days_ago_min"]["options"]["25"]
    chunk: Optional[int] = ExpiredChecker_args["chunk"]["options"]["None"]
    change_headers: Optional[int] = ExpiredChecker_args["change_headers"]["options"][
        "None"
    ]
    resume: Optional[bool] = ExpiredChecker_args["resume"]["options"]["False"]
    repeats: Optional[int] = ExpiredChecker_args["repeats"]["options"]["1"]
    repeats_timeout: Optional[float] = ExpiredChecker_args["repeats_timeout"][
        "options"
    ]["5"]
    main_loop_timeout: Optional[float] = ExpiredChecker_args["main_loop_timeout"][
        "options"
    ]["1"]

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


async def map_gen(
    request,
    jobs,
    sql,
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    kwds: dict = {}
    if "page_map" in rq_args["map_type"] and (
        job_id_list := [job.job_id for job in jobs["items"]] if jobs else []
    ):
        kwds = dict(job_id_list=job_id_list)
    elif "query_map" in rq_args["map_type"]:
        kwds = dict(jobs_df=load_df(sql=sql))
    elif "full_map" in rq_args["map_type"]:
        kwds = {}
    m, _, _, _ = await exec_block(generate_map, **kwds)
    return m.get_root()._repr_html_()


def generate_analytics(
    jobs_df: Optional[DataFrame] = None, job_id_list: Optional[list[str]] = None
) -> JSONResponse:
    plots: dict[str, Figure] = Analytics(jobs_df, job_id_list).plot_all()
    return jsonResp(OrderedDict({k: jsonify_plotly(v) for k, v in plots.items()}))


async def analytics_gen(
    request,
    jobs,
    sql,
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    kwds: dict = {}
    if "page_analytics" in rq_args["analytics_type"] and (
        job_id_list := [job.job_id for job in jobs["items"]] if jobs else []
    ):
        kwds = dict(job_id_list=job_id_list)
    elif "query_analytics" in rq_args["analytics_type"]:
        kwds = dict(jobs_df=load_df(sql=sql))
    elif "full_analytics" in rq_args["analytics_type"]:
        kwds = {}
    return await exec_block(generate_analytics, **kwds)
