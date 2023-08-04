import importlib
from logging import Logger
from pprint import pformat
from starlette.templating import _TemplateResponse
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse

import job_config as jc
from job_seeker import seeker_args, update_days_ago
from job_seeker.ip_seek import ip_seeker

from ... import db
from ...db.models import Seeker
from ...logger import logdef
from ..utils import (
    column_operators,
    distinct_v_html,
    get_cols,
    last_db_entry,
    order_filter,
    render_html,
    setup_filters,
    exec_block
)
from .seeker_exec import seeker_exec
from . import router

# nest_asyncio.apply()
log: Logger = logdef(__name__)


@router.on_event("startup")
async def collector_startup() -> None:
    await exec_block(update_days_ago, 'seeker')


@router.get("/", response_class=HTMLResponse)
async def seeker_index(
    request: Request,
) -> _TemplateResponse:
    return render_html(
        "seeker/index.html",
        {
            "exec_args": seeker_args,
            "cols": get_cols(Seeker),
            "col_opers": column_operators(),
        },
    )


@router.get("/api/exec")
async def seeker_api_exec(request: Request) -> str:
    rq_args: dict[str, str] = dict(request.query_params)
    importlib.reload(jc)
    log.info('\n rq_args: %s', pformat(rq_args))
    ip = await ip_seeker().get_ip_async()
    summary = await exec_block(
        seeker_exec,
        rq_args, jc.job_titles, jc.not_words, jc.locations, ip=ip
    )

    return f"<pre>{summary}</pre>"



@router.get("/api/last_db_entry")
async def seeker_api_last_db_entry(request: Request, ses=Depends(db.get_ses)) -> str:
    return await last_db_entry(db.models.Subquery, ses)


@router.get("/api/distinct_values")
async def seeker_api_distinct_values(request: Request, ses=Depends(db.get_ses)) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    if field := rq_params.get("distinct_values"):
        html: str = await distinct_v_html(field, Seeker, ses)
        return html
    return "something went wrong"


@router.get("/api/items", response_class=HTMLResponse)
@router.get("/api/items/{page}", response_class=HTMLResponse)
async def seeker_api_items(
    request: Request,
    ses=Depends(db.get_ses),
    page: int = 1,
) -> _TemplateResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    jobs = {}
    cols: list[str] = [col.name for col in Seeker.__table__.c]

    per_page: int = int(rq_args.get("per_page") or 5)

    table = Seeker
    filter_args = await setup_filters(rq_args, table)
    order = await order_filter(rq_args, table)
    sql = db.select(table).filter(db.and_(True, *filter_args)).order_by(order)
    jobs = await db.paginator.AsyncPagination(
        page=page,
        per_page=per_page,
        max_per_page=100,
        error_out=True,
        count=True,
        rq_args=rq_args,
        session=ses,
        select=sql,
    )

    # print(pformat(jobs))
    return render_html(
        "seeker/seeker_items.html",
        {
            "jobs": jobs,
            "cols": cols,
            "page": page,
        },
    )  


# rename later
@router.get("/api/log_stream")
async def api_log_stream(
    request: Request,
) -> str:
    # sql = db.select(Subquery).order_by(Subquery.Date_log.desc()).limit(1)
    # last_entry = db.session.execute(sql).scalar()
    # td: datetime.timedelta = datetime.datetime.utcnow() - last_entry.Date_log
    # days = td.days
    # hours, remainder = divmod(td.seconds, 3600)
    # minutes, seconds = divmod(remainder, 60)
    # return f"{days} Days - {hours} hours - {minutes} minutes - {seconds}secs"
    return "ok works"
