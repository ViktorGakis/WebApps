from logging import Logger
from pprint import pformat

from fastapi import Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import _TemplateResponse

from ... import db
from ...logger import logdef
from ..utils import (
    btn_update,
    column_operators,
    distinct_v_html,
    get_cols,
    jsonResp,
    order_filter,
    render_html,
    setup_filters,
)
from . import router

log: Logger = logdef(__name__)
sql = None
jobs = {}


# @router.get("/", response_class=HTMLResponse)
# async def jobs_index(
#     request: Request,
# ) -> _TemplateResponse:
#     return render_html(
#         "index.html",
#         {
#             "cols": get_cols(db.models.jobsch.Job),
#             "col_opers": column_operators(),
#         },
#     )


# @router.options("/api/items/cols", response_class=HTMLResponse)
@router.get("/api/items/cols", response_class=HTMLResponse)
async def jobs_api_items_cols(
    request: Request,
    table: str = Query("db.models.jobsch.Job", description="The name of table"),
) -> JSONResponse:
    table_name = eval(table)
    form_dict: dict[str, list] = {
        "cols": get_cols(table_name),
    }
    print(f"{form_dict=}")
    return jsonResp(form_dict)


# @router.options("/api/items/opers", response_class=HTMLResponse)
@router.get("/api/items/opers", response_class=HTMLResponse)
async def jobs_api_items_opers(
    request: Request,
) -> JSONResponse:
    form_dict: dict[str, list] = {
        "col_opers": column_operators(),
    }
    print(f"{form_dict=}")
    return jsonResp(form_dict)


@router.get("/api/distinct_values")
@router.post("/api/distinct_values")
async def jobs_api_distinct_values(
    request: Request,
    ses=Depends(db.get_ses),
    table: str = Query("db.models.jobsch.Job", description="The name of table"),
    field: str = Query(..., description="Column name"),
) -> JSONResponse:
    table_name = eval(table)
    html: str = await distinct_v_html(field.strip(), table_name, ses)
    return jsonResp({"data": html})


@router.get("/api/retrieve", response_class=HTMLResponse)
async def jobs_api(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    table = db.models.jobsch.Job
    date_col = getattr(table, "publication_date")
    sql = db.select(table).order_by(date_col.desc()).limit(5)
    jobs = (await ses.execute(sql)).scalars()
    jobs = [job._dict() for job in jobs]
    return jsonResp({"data": jobs})


@router.get("/api/items", response_class=HTMLResponse)
@router.get("/api/items/{page}", response_class=HTMLResponse)
async def jobs_api_items(
    request: Request,
    ses=Depends(db.get_ses),
    page: int = 1,
) -> JSONResponse:
    global jobs, sql
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    table = db.models.jobsch.Job

    filter_args: list = []
    per_page: int = int(rq_args.get("per_page") or 5)
    filter_args = await setup_filters(rq_args, table)

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
    return jsonResp({"data": jobs})


@router.get("/api/item/save", response_class=HTMLResponse)
async def jobs_api_save(
    request: Request,
    job_id: str = Query(..., description="The job ID"),
    ses=Depends(db.get_ses),
) -> JSONResponse:
    btn_type = "saved"
    table = db.models.jobsch.Job
    job = (await ses.execute(db.select(table).filter(table.job_id == job_id))).scalar()
    val_old = getattr(job, btn_type)
    # log.debug('val_old: %s', val_old)
    setattr(job, f"{btn_type}", 0 if val_old else 1)
    val_new = getattr(job, btn_type)
    await ses.commit()
    # log.debug('val_new: %s', val_new)
    return jsonResp({"job_id": job_id, "saved": val_new})


# @router.get("/api/item/save", response_class=HTMLResponse)
# async def jobs_api_save(
#     request: Request,
#     ses=Depends(db.get_ses),
# ) -> JSONResponse:
#     rq_args: dict[str, str] = dict(request.query_params)
#     return jsonResp({"saved_status": await btn_update(db.models.jobsch.Job, rq_args, "saved", ses)})


@router.get("/api/item/like", response_class=HTMLResponse)
async def jobs_api_dis(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    return jsonResp(
        {"like_status": await btn_update(db.models.jobsch.Job, rq_args, "liked", ses)}
    )


@router.get("/api/item/apply", response_class=HTMLResponse)
async def jobs_api_apply(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    applied_status: int = await package_application(rq_args, jobs, ses)
    # applied_status = 0
    return jsonResp({"applied_status": applied_status})


@router.get("/api/item/expired", response_class=HTMLResponse)
async def jobs_api_expired(
    request: Request,
    ses=Depends(db.get_ses),
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    return jsonResp(
        {
            "expired_status": await btn_update(
                db.models.jobsch.Job, rq_args, "expired", ses=ses
            )
        }
    )
