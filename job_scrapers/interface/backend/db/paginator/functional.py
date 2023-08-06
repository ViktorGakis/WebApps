from __future__ import annotations

import sqlalchemy as sa
from fastapi import HTTPException

from .utils import (
    first,
    has_next,
    has_prev,
    iter_pages,
    last,
    next_num,
    pages,
    prepare_page_args,
    prev_num,
    query_count,
    query_items,
    total,
)


async def AsyncPagination(
    page: int | None = None,
    per_page: int | None = None,
    max_per_page: int | None = None,
    error_out: bool = True,
    count: bool = True,
    rq_args: dict | None = None,
    select: sa.select = None,
    session: sa.orm.Session = None,
):
    attrs = dict()
    page, per_page = await prepare_page_args(
        page=page,
        per_page=per_page,
        max_per_page=max_per_page,
        error_out=error_out,
        rq_args=rq_args,
    )

    attrs["page"] = page
    attrs["per_page"] = per_page

    items = await query_items(attrs["page"], attrs["per_page"], select, session)

    if not items and page != 1 and error_out:
        raise HTTPException(status_code=404, detail="Items not found")

    attrs["items"] = items
    attrs["first"] = await first(attrs["items"], attrs["page"], attrs["per_page"])
    attrs["last"] = await last(attrs["first"], attrs["items"])
    attrs["total"] = await total(count, query_count, select, session)
    attrs["pages"] = await pages(attrs["total"], attrs["per_page"])
    attrs["has_prev"] = await has_prev(attrs["page"])
    attrs["prev_num"] = await prev_num(attrs["has_prev"], attrs["page"])
    attrs["has_next"] = await has_next(attrs["page"], attrs["pages"])
    attrs["next_num"] = await next_num(attrs["has_next"], attrs["page"])
    attrs["iter_pages"] = iter_pages(attrs["page"], attrs["pages"])
    return attrs

