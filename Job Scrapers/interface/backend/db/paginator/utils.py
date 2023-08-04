from __future__ import annotations

import asyncio
from math import ceil
from typing import Any

import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def prepare_page_args(
    *,
    page: int | None = None,
    per_page: int | None = None,
    max_per_page: int | None = None,
    error_out: bool = True,
    rq_args: dict | None = None,
) -> tuple[int, int]:
    if rq_args:
        if page is None:
            try:
                page = int(rq_args.get("page", 1))
            except (TypeError, ValueError):
                if error_out:
                    raise HTTPException(status_code=404, detail="Items not found")

                page = 1

        if per_page is None:
            try:
                per_page = int(rq_args.get("per_page", 20))
            except (TypeError, ValueError):
                if error_out:
                    raise HTTPException(status_code=404, detail="Items not found")

                per_page = 20
    else:
        if page is None:
            page = 1

        if per_page is None:
            per_page = 20

    if max_per_page is not None:
        per_page = min(per_page, max_per_page)

    if page < 1:
        if error_out:
            raise HTTPException(status_code=404, detail="Items not found")
        else:
            page = 1

    if per_page < 1:
        if error_out:
            raise HTTPException(status_code=404, detail="Items not found")
        else:
            per_page = 20

    return page, per_page


async def query_offset(page, per_page) -> int:
    """The index of the first item to query, passed to ``offset()``.

    :meta private:

    .. versionadded:: 3.0
    """
    return (page - 1) * per_page


async def query_items(page, per_page, select, session) -> list[Any]:
    _query_offset = await query_offset(page, per_page)
    select = select.limit(per_page).offset(_query_offset)
    if isinstance(session, AsyncSession):
        res = await session.execute(select)
        return list(res.unique().scalars())
    return list(session.execute(select).unique().scalars())


async def last(first, items) -> int:
    """The number of the last item on the page, starting from 1, inclusive, or 0 if
    there are no items.

    .. versionadded:: 3.0
    """
    first = first
    return max(first, first + len(items) - 1)


async def first(items, page, per_page) -> int:
    """The number of the first item on the page, starting from 1, or 0 if there are
    no items.

    .. versionadded:: 3.0
    """
    if len(items) == 0:
        return 0

    return (page - 1) * per_page + 1


async def query_count(select, session) -> int:
    sub = select.options(sa.orm.lazyload("*")).order_by(None).subquery()
    sql = sa.select(sa.func.count()).select_from(sub)
    if isinstance(session, AsyncSession):
        return (await session.execute(sql)).scalar()
    return session.execute(sql).scalar()


async def total(count, query_count, select, session):
    """The total number of items across all pages."""
    if not count:
        total = None
    if asyncio.iscoroutinefunction(query_count):
        total = await query_count(select, session)
    else:
        total = query_count(select, session)
    return total


async def pages(total, per_page) -> int:
    """The total number of pages."""
    if total == 0 or total is None:
        return 0

    return ceil(total / per_page)


async def has_prev(page) -> bool:
    """``True`` if this is not the first page."""
    return page > 1


async def prev_num(has_prev, page) -> int | None:
    """The previous page number, or ``None`` if this is the first page."""
    if not has_prev:
        return None

    return page - 1


async def has_next(page, pages) -> bool:
    """``True`` if this is not the last page."""
    return page < pages


async def next_num(has_next, page) -> int | None:
    """The next page number, or ``None`` if this is the last page."""
    if not has_next:
        return None

    return page + 1


def iter_pages(page, pages, left_edge=1, right_edge=1, left_current=5, right_current=5):
    """Yield page numbers for a pagination widget. Skipped pages between the edges
    and middle are represented by a ``None``.

    For example, if there are 20 pages and the current page is 7, the following
    values are yielded.

    .. code-block:: python

        1, 2, None, 5, 6, 7, 8, 9, 10, 11, None, 19, 20

    :param left_edge: How many pages to show from the first page.
    :param left_current: How many pages to show left of the current page.
    :param right_current: How many pages to show right of the current page.
    :param right_edge: How many pages to show from the last page.
    """
    pages_end = pages + 1

    if pages_end == 1:
        return

    left_end = min(1 + left_edge, pages_end)
    yield from range(1, left_end)

    if left_end == pages_end:
        return

    mid_start = max(left_end, page - left_current)
    mid_end = min(page + right_current + 1, pages_end)

    if mid_start - left_end > 0:
        yield None

    yield from range(mid_start, mid_end)

    if mid_end == pages_end:
        return

    right_start = max(mid_end, pages_end - right_edge)

    if right_start - mid_end > 0:
        yield None

    yield from range(right_start, pages_end)
