from logging import Logger
from pprint import pformat

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from job_seeker import locator_gmap, locator_gmap_args, locator_nom_args
from job_seeker.locator.main_script import locator_nom

from ... import db
from ...db.models import Locator
from ...logger import logdef
from ..utils import (
    column_operators,
    distinct_v_html,
    exec_block,
    get_cols,
    order_filter,
    render_html,
    setup_filters,
)
from . import router
from .exec_locators import ExecArgsMaps, ExecArgsNom, parse_locator_map_args, parse_locator_nom_args

log: Logger = logdef(__name__)

TABLE: Locator = Locator

# @router.on_event("startup")
# async def collector_startup() -> None:
#     await exec_block(update_days_ago, 'jobs')


@router.get("/", response_class=HTMLResponse)
async def locator_index(
    request: Request,
) -> _TemplateResponse:
    return render_html(
        "locator/index.html",
        {
            "cols": get_cols(TABLE),
            "col_opers": column_operators(),
            "exec_args_locator_gmap": locator_gmap_args,
            "exec_args_locator_nom": locator_nom_args,
        },
    )


@router.get("/api/exec/locatorgmap")
async def locator_api_exec_gmap(request: Request) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    exec_args: ExecArgsMaps | None = await parse_locator_map_args(rq_params)
    # refresh conscent cookies when needed
    cookies: dict[str, str] = {
        # "__Secure-ENID":"11.SE=k3wqqo8ybqhBQ7U6ak68PTzYpHMe4EQjqUp5An6C6wmQcgHwbyTdGetETQfUfQzIz3NJORRKheowwNdbmT43RsdOdFFTBwWv6bgJUYHEU1wzwOIwVGcL6Sw5QE16xWp2TvvX4pVOctLGLxAr38XZcgy79VAnB4VTUMQ1vzDN5Uo",
        "SOCS": "CAESOAgEEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwMzIxLjA1X3AwGgVlbi1HQiACGgYIgLmDoQY",
        "CONSENT":"PENDING+796",
        }
    
    summary: str = await locator_gmap(
        **exec_args.dict(),
        session_dict=dict(cookies=cookies)
    )
    return f"<pre>{summary}</pre>"

@router.get("/api/exec/locatornom")
async def locator_api_exec_nom(request: Request) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    exec_args: ExecArgsNom | None = await parse_locator_nom_args(rq_params)
    summary = await exec_block(locator_nom, **exec_args.dict())
    return f"<pre>{summary}</pre>"



@router.get("/api/distinct_values")
@router.post("/api/distinct_values")
async def locator_api_distinct_values(request: Request, ses=Depends(db.get_ses)) -> str:
    rq_params: dict[str, str] = dict(request.query_params)
    if field := rq_params.get("distinct_values"):
        html: str = await distinct_v_html(field.strip(), TABLE, ses)
        return html
    return "something went wrong"


@router.get("/api/items", response_class=HTMLResponse)
@router.get("/api/items/{page}", response_class=HTMLResponse)
async def locator_api_items(
    request: Request,
    ses=Depends(db.get_ses),
    page: int = 1,
) -> _TemplateResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    jobs = {}
    cols: list[str] = [col.name for col in TABLE.__table__.c]

    per_page: int = int(rq_args.get("per_page") or 5)
    
    filter_args = await setup_filters(rq_args, TABLE)
    order = await order_filter(rq_args, TABLE)
    sql = db.select(TABLE).filter(db.and_(True, *filter_args)).order_by(order)
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
        "locator/jobs_items.html",
        {
            "jobs": jobs,
            "cols": cols,
            "page": page,
        },
    )
