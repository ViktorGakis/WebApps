from logging import Logger
from pprint import pformat

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import _TemplateResponse

from job_config import motivation_letter
from job_seeker import (
    ExpiredChecker,
    ExpiredChecker_args,
    ip_seeker,
    locator_gmap_args,
    locator_nom_args,
    update_days_ago,
    update_jobs,
)

from ... import db
from ...db.models import Job
from ...logger import logdef
from ..utils import (
    btn_update,
    column_operators,
    country_filter,
    distinct_v_html,
    exec_block,
    get_cols,
    job_descr_process,
    jsonResp,
    order_filter,
    package_application,
    render_html,
    retrieve_companies,
    setup_filters,
)
from . import router
from .exec import analytics_gen, map_gen, parse_exec_args

log: Logger = logdef(__name__)
ip_seek: ip_seeker = ip_seeker()
exec_func: ExpiredChecker | None = None
sql = None
jobs = {}


@router.on_event("startup")
async def jobs_startup() -> None:
    await exec_block(update_days_ago, "jobs")


@router.get("/", response_class=HTMLResponse)
async def jobs_index(
    request: Request,
) -> _TemplateResponse:
    return render_html(
        "jobs/index.html",
        {
            "cols": get_cols(Job),
            "col_opers": column_operators(),
            "exec_args_expiredchecker": ExpiredChecker_args,
            "exec_args_locator_gmap": locator_gmap_args,
            "exec_args_locator_nom": locator_nom_args,
            "country_filter": True,
        },
    )


@router.get("/api/exec/jobs/start")
async def jobs_api_exec_start(request: Request) -> str:
    summary = await exec_block(update_jobs)
    return f"<pre>{summary}</pre>"


@router.get("/api/exec/jobs/stop")
async def jobs_api_exec_stop(request: Request) -> str:
    # summary = await exec_block(update_jobs)
    return f"okboistop"


async def expired_checker_exec(request) -> str:
    global ip_seek, exec_func
    rq_args: dict[str, str] = dict(request.query_params)
    log.info("\n rq_args: %s", pformat(rq_args))
    ip: str = await ip_seek.get_ip_async()
    if exec_args := await parse_exec_args(rq_args):
        log.info("exec_args: %s", pformat(exec_args))
        exec_func = ExpiredChecker(
            **exec_args.dict(),
            headers=None,
            cookies=None,
            ip=ip,
        )
        await exec_block(exec_func.start)

    return await exec_func.summaries_html()


@router.get("/api/exec/expirecheck/start")
async def jobs_api_exec_expiredcheck_start(request: Request) -> str:
    global ip_seek, exec_func
    return await expired_checker_exec(request)


@router.get("/api/exec/expirecheck/stop")
async def jobs_api_exec_expiredcheck_stop(request: Request) -> str:
    global ip_seek, exec_func
    if isinstance(exec_func, ExpiredChecker):
        if not exec_func.switch:
            return "Already Stopped."
        exec_func.switch = False
        return "Stopping Sequence engaged."
    return f"exec_func:{exec_func.__class__}, NOT instantiated."


@router.get("/api/distinct_values")
@router.post("/api/distinct_values")
async def jobs_api_distinct_values(request: Request, ses=Depends(db.get_ses)) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    if field := rq_params.get("distinct_values"):
        html: str = await distinct_v_html(field.strip(), Job, ses)
        return html
    return "something went wrong"


@router.get("/api/items", response_class=HTMLResponse)
@router.get("/api/items/{page}", response_class=HTMLResponse)
async def jobs_api_items(
    request: Request,
    ses=Depends(db.get_ses),
    page: int = 1,
) -> _TemplateResponse:
    global jobs, sql
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    table = Job

    cols: list[str] = [col.name for col in table.__table__.c]
    filter_args: list = []
    per_page: int = int(rq_args.get("per_page") or 5)
    filter_args = await setup_filters(rq_args, table)
    filter_args.append(await country_filter(rq_args))

    order = await order_filter(rq_args, table)
    sql = db.select(table).filter(db.and_(True, *filter_args)).order_by(order)
    jobs = await db.paginator.AsyncPagination(
        page=page,
        per_page=per_page,
        max_per_page=per_page,
        error_out=True,
        count=True,
        rq_args=rq_args,
        session=ses,
        select=sql,
    )
    await exec_block(job_descr_process, jobs, table)
    await retrieve_companies(jobs, table, ses)

    return render_html(
        "jobs/jobs_items.html",
        {
            "jobs": jobs,
            "cols": cols,
            "page": page,
            "motivation_letter": motivation_letter,
        },
    )


@router.get("/api/folium", response_class=HTMLResponse)
async def jobs_api_folium(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    return await map_gen(request, jobs, sql)


@router.get("/api/analytics", response_class=HTMLResponse)
async def jobs_api_analytics(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    return await analytics_gen(request, jobs, sql)


@router.get("/api/save", response_class=HTMLResponse)
async def jobs_api_save(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    return jsonResp({"saved_status": await btn_update(Job, rq_args, "saved", ses)})


@router.get("/api/dis", response_class=HTMLResponse)
async def jobs_api_dis(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    return jsonResp({"dis_status": await btn_update(Job, rq_args, "fav", ses)})


@router.get("/api/apply", response_class=HTMLResponse)
async def jobs_api_apply(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    applied_status: int = await package_application(rq_args, jobs, ses)
    # applied_status = 0
    return jsonResp({"applied_status": applied_status})


@router.get("/api/expired", response_class=HTMLResponse)
async def jobs_api_expired(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    return jsonResp(
        {
            "expired_status": await btn_update(
                Job, rq_args, "expired", ses=ses, date_change=False
            )
        }
    )
