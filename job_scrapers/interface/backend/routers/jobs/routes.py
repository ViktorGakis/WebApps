from logging import Logger
from pprint import pformat
from typing import Any, Optional

from fastapi import Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import _TemplateResponse

from ... import db
from ...logger import logdef
from ..utils import (
    btn_upd,
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


@router.get("/api/items/cols", response_class=HTMLResponse)
async def jobs_api_items_cols(
    request: Request,
    table: str = Query(..., description="The name of the table"),
) -> JSONResponse:
    table_name = eval(table)
    form_dict: dict[str, list] = {
        "cols": get_cols(table_name),
    }
    print(f"{form_dict=}")
    return jsonResp(form_dict)


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
    table: str = Query(...),
    field: str = Query(...),
) -> JSONResponse:
    print(
        f"""
        {table=}
        {field=}
        """
    )
    table_name = eval(table)
    html: str = await distinct_v_html(field.strip(), table_name, ses)
    print(f"{html}=")
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
# @router.get("/api/items/{page}", response_class=HTMLResponse)
async def jobs_api_items(
    request: Request, ses=Depends(db.get_ses), page: int = 1, table: str = Query(...)
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    log.debug("\n rq_args \n %s", pformat(rq_args))
    table = eval(table)
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
    ses=Depends(db.get_ses),
    table: str = Query(..., description="The sqlalchemy table class"),
    job_id: str = Query(..., description="The job ID"),
    # liked: int = Query(..., description="The liked value"),
) -> JSONResponse:
    identifier = "job_id"
    identifier_value: str = job_id
    target_col = "saved"
    # target_val: Any = liked
    print(f"{identifier_value=}")
    job = await btn_upd(
        table,
        identifier,
        identifier_value,
        target_col,
        {0: 1, None: 1, 1: 0},
        ses,
    )
    print(f'{job["saved"]=}')
    return jsonResp(job)


@router.get("/api/item/like", response_class=HTMLResponse)
async def jobs_api_like(
    request: Request,
    ses=Depends(db.get_ses),
    table: str = Query(..., description="The sqlalchemy table class"),
    job_id: str = Query(..., description="The job ID"),
    # liked: int = Query(..., description="The liked value"),
) -> JSONResponse:
    identifier = "job_id"
    identifier_value: str = job_id
    target_col = "liked"
    # target_val: Any = liked
    print(f"{identifier_value=}")
    job = await btn_upd(
        table,
        identifier,
        identifier_value,
        target_col,
        {0: 1, None: 1, -1: 1, 1: 0},
        ses,
    )
    print(f"{job['liked']=}")
    return jsonResp(job)


@router.get("/api/item/dislike", response_class=HTMLResponse)
async def jobs_api_dislike(
    request: Request,
    ses=Depends(db.get_ses),
    table: str = Query(..., description="The sqlalchemy table class"),
    job_id: str = Query(..., description="The job ID"),
    # liked: int = Query(..., description="The liked value"),
) -> JSONResponse:
    identifier = "job_id"
    identifier_value: str = job_id
    target_col = "liked"
    # target_val: Any = liked
    print(f"{identifier_value=}")
    job = await btn_upd(
        table,
        identifier,
        identifier_value,
        target_col,
        {0: -1, None: -1, 1: -1, -1: 0},
        ses,
    )
    print(f"{job['liked']=}")
    return jsonResp(job)


@router.get("/api/item/apply", response_class=HTMLResponse)
async def jobs_api_apply(
    request: Request,
    ses=Depends(db.get_ses),
    table: str = Query(..., description="The sqlalchemy table class"),
    job_id: str = Query(..., description="The job ID"),
    # liked: int = Query(..., description="The liked value"),
) -> JSONResponse:
    identifier = "job_id"
    identifier_value: str = job_id
    target_col = "applied"
    # target_val: Any = liked
    print(f"{identifier_value=}")
    job = await btn_upd(
        table,
        identifier,
        identifier_value,
        target_col,
        {0: 1, None: 1, 1: 0},
        ses,
    )
    print(f"{job['applied']=}")
    return jsonResp(job)


@router.get("/api/item/expire", response_class=HTMLResponse)
async def jobs_api_expire(
    request: Request,
    ses=Depends(db.get_ses),
    table: str = Query(..., description="The sqlalchemy table class"),
    job_id: str = Query(..., description="The job ID"),
    # liked: int = Query(..., description="The liked value"),
) -> JSONResponse:
    identifier = "job_id"
    identifier_value: str = job_id
    target_col = "expired"
    # target_val: Any = liked
    print(f"{identifier_value=}")
    job = await btn_upd(
        table,
        identifier,
        identifier_value,
        target_col,
        {0: 1, None: 1, 1: 0},
        ses,
    )
    print(f"{job['expired']=}")
    return jsonResp(job)
