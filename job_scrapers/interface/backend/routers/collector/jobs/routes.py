from logging import Logger
from pprint import pformat

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import _TemplateResponse

from job_seeker import collector_jobs_args, update_days_ago
from job_seeker.ip_seek.ip_main import ip_seeker

from .... import db
from ....db.models import Collector
from ....logger import logdef
from ...utils import (
    column_operators,
    distinct_v_html,
    exec_block,
    get_cols,
    job_descr_process,
    jsonResp,
    order_filter,
    render_html,
    retrieve_companies,
    setup_filters,
)
from . import router
from .collector_exec import collector_exec

log: Logger = logdef(__name__)
ip_seek: ip_seeker = ip_seeker()


# @router.on_event("startup")
# async def collector_startup() -> None:
#     await exec_block(update_days_ago, 'collector')



@router.get("/", response_class=HTMLResponse)
async def collector_jobs_index(
    request: Request,
) -> _TemplateResponse:
    return render_html(
        "collector/jobs/index.html",
        {
            "exec_args": collector_jobs_args,
            "cols": get_cols(Collector),
            "col_opers": column_operators(),
        },
    )


@router.get("/api/exec/start")
async def collector_jobs_api_exec_start(request: Request) -> str:
    global ip_seek
    rq_args: dict[str, str] = dict(request.query_params)
    log.info("\n rq_args: %s", pformat(rq_args))
    ip: str = await ip_seek.get_ip_async()
    summary = await exec_block(collector_exec, rq_args, ip=ip)
    return f"<pre>{summary}</pre>"

@router.get("/api/exec/stop")
async def collector_jobs_api_exec_stop(request: Request) -> str:
    # global ip_seek
    # rq_args: dict[str, str] = dict(request.query_params)
    # log.info("\n rq_args: %s", pformat(rq_args))
    # ip: str = await ip_seek.get_ip_async()
    # summary = await exec_block(collector_exec, rq_args, ip=ip)
    return f"okboi"

@router.get("/api/distinct_values")
@router.post("/api/distinct_values")
async def collector_jobs_api_distinct_values(
    request: Request, ses=Depends(db.get_ses)
) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    if field := rq_params.get("distinct_values"):
        html: str = await distinct_v_html(field.strip(), Collector, ses)
        return html
    return "something went wrong"


@router.get("/api/items", response_class=HTMLResponse)
@router.get("/api/items/{page}", response_class=HTMLResponse)
async def collector_jobs_api_items(
    request: Request,
    ses=Depends(db.get_ses),
    page: int = 1,
) -> _TemplateResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    jobs = {}
    cols: list[str] = [col.name for col in Collector.__table__.c]

    per_page: int = int(rq_args.get("per_page") or 5)

    table = Collector
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

    await exec_block(job_descr_process, jobs, table)
    await retrieve_companies(jobs, table, ses)
    return render_html(
        "collector/jobs/collector_items.html",
        {
            "jobs": jobs,
            "cols": cols,
            "page": page,
        },
    )


@router.get("/api/save", response_class=HTMLResponse)
async def collector_jobs_api_save(
    request: Request,
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    if job_id := rq_args.get("job_id"):
        pass
    d: dict[str, int] = {"saved_status": 1}
    return jsonResp(d)


@router.get("/api/apply", response_class=HTMLResponse)
async def collector_jobs_api_apply(
    request: Request,
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    if job_id := rq_args.get("job_id"):
        pass
    d: dict[str, int] = {"applied_status": 1}
    return jsonResp(d)


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
