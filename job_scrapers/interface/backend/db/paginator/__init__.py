from .classes import Pagination, SelectPagination
from sqlalchemy.sql import Select
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .functional import AsyncPagination


async def paginate(
    select: Select[Any],
    session: AsyncSession|Session,
    *,
    page: int | None = None,
    per_page: int | None = None,
    max_per_page: int | None = None,
    error_out: bool = True,
    count: bool = True,
    rq_args: dict|None = None,
    loop = None
) -> Pagination:
    """Apply an offset and limit to a select statment based on the current page and
    number of items per page, returning a :class:`.Pagination` object.
    The statement should select a model class, like ``select(User)``. This applies
    ``unique()`` and ``scalars()`` modifiers to the result, so compound selects will
    not return the expected results.
    :param select: The ``select`` statement to paginate.
    :param page: The current page, used to calculate the offset. Defaults to the
        ``page`` query arg during a request, or 1 otherwise.
    :param per_page: The maximum number of items on a page, used to calculate the
        offset and limit. Defaults to the ``per_page`` query arg during a request,
        or 20 otherwise.
    :param max_per_page: The maximum allowed value for ``per_page``, to limit a
        user-provided value. Use ``None`` for no limit. Defaults to 100.
    :param error_out: Abort with a ``404 Not Found`` error if no items are returned
        and ``page`` is not 1, or if ``page`` or ``per_page`` is less than 1, or if
        either are not ints.
    :param count: Calculate the total number of values by issuing an extra count
        query. For very complex queries this may be inaccurate or slow, so it can be
        disabled and set manually if necessary.
    .. versionchanged:: 3.0
        The ``count`` query is more efficient.
    .. versionadded:: 3.0
    """
    return SelectPagination(
        select=select,
        session=session,
        page=page,
        per_page=per_page,
        max_per_page=max_per_page,
        error_out=error_out,
        count=count,
        rq_args=rq_args,
        loop=loop
    )