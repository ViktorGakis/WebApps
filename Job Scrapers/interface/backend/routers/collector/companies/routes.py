from logging import Logger
from pprint import pformat

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import _TemplateResponse

from job_seeker import collector_companies_args
from job_seeker.ip_seek.ip_main import ip_seeker
from job_seeker.collector.collector_companies_main import CollectorCompany
from .... import db
from ....db.models import Company
from ....logger import logdef
from ...utils import (
    column_operators,
    distinct_v_html,
    exec_block,
    get_cols,
    jsonResp,
    order_filter,
    render_html,
    setup_filters,
)
from . import router
from .companies_exec import collector_companies_exec, parse_exec_args

log: Logger = logdef(__name__)
ip_seek: ip_seeker = ip_seeker()
exec_func: CollectorCompany|None = None

@router.get("/", response_class=HTMLResponse)
async def collector_companies_index(
    request: Request, 
    # the request var is silently passed into render html
    # see render html definition for details
) -> _TemplateResponse:
    return render_html(
        "collector/companies/index.html",
        {
            "exec_args": collector_companies_args,
            "cols": get_cols(Company),
            "col_opers": column_operators(),
        },
    )


@router.get("/api/exec/start")
async def collector_companies_api_exec_start(request: Request) -> str:
    global ip_seek, exec_func
    rq_args: dict[str, str] = dict(request.query_params)
    log.info("\n rq_args: %s", pformat(rq_args))
    ip: str = await ip_seek.get_ip_async()
    if (exec_args := await parse_exec_args(rq_args)):
        log.info('exec_args: %s', pformat(exec_args))
        exec_func = CollectorCompany(
            **exec_args.dict(),
            headers=None,
            cookies=None,
            ip=ip,            
        )    
        await exec_block(exec_func.start)

    return await exec_func.summaries_html()


@router.get("/api/exec/stop")
async def collector_companies_api_exec_stop(request: Request) -> str:
    global ip_seek, exec_func
    if isinstance(exec_func, CollectorCompany):
        if not exec_func.switch:
            return 'Already Stopped.'
        exec_func.switch = False
        return 'Stopping Sequence engaged.'
    return f'exec_func:{exec_func.__class__}, NOT instantiated.'

@router.get("/api/distinct_values")
@router.post("/api/distinct_values")
async def collector_companies_api_distinct_values(
    request: Request, ses=Depends(db.get_ses)
) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    if field := rq_params.get("distinct_values"):
        html: str = await distinct_v_html(field.strip(), Company, ses)
        return html
    return "something went wrong"


@router.get("/api/items", response_class=HTMLResponse)
@router.get("/api/items/{page}", response_class=HTMLResponse)
async def collector_companies_api_items(
    request: Request,
    ses=Depends(db.get_ses),
    page: int = 1,
) -> _TemplateResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    jobs = {}
    cols: list[str] = [col.name for col in Company.__table__.c]

    per_page: int = int(rq_args.get("per_page") or 5)

    table = Company
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

    return render_html(
        "collector/companies/companies_items.html",
        {
            "jobs": jobs,
            "cols": cols,
            "page": page,
        },
    )


@router.get("/api/save", response_class=HTMLResponse)
async def collector_companies_api_save(
    request: Request,
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    if job_id := rq_args.get("job_id"):
        pass
    d: dict[str, int] = {"saved_status": 1}
    return jsonResp(d)

