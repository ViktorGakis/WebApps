import asyncio
import json
import operator as op
import re
from asyncio import AbstractEventLoop, get_running_loop
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextvars import Context, copy_context
from datetime import datetime, timedelta, timezone
from functools import partial
from inspect import currentframe
from logging import FileHandler, Logger
from pathlib import Path
from typing import Any, Callable, Literal, Optional

import plotly.graph_objects as go
from bs4 import BeautifulSoup, NavigableString, Tag
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from plotly.utils import PlotlyJSONEncoder
from sqlalchemy import Column
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.expression import ColumnOperators
from starlette.templating import _TemplateResponse

# from job_seeker import get_country_str, get_jobs_from_country
from .. import db
from ..config import APISettings, get_api_settings
from ..logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


def jsonify_plotly(fig: go.Figure) -> str:
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def get_outer_scope_var(var_type: Any) -> Any | None:
    """Returns the first var of type var_type from the outerscope."""
    frame = currentframe().f_back.f_back
    if vars := [v for k, v in frame.f_locals.items() if isinstance(v, var_type)]:
        return vars[0]


def jsonResp(d: dict) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(d))


def render_html(
    template: str, context_vars: Optional[dict] = None
) -> _TemplateResponse:
    request: Request = get_outer_scope_var(Request)
    context_dict: dict[str, Request] = dict(request=request) | (context_vars or {})
    return request.app.state.templates.TemplateResponse(template, context_dict)


def op_func(oprtr: str) -> Any | None:
    """
    Retrieves all the operators from the operator package
    by their string representation

    Args:
        oprtr (str): Operator in string format.

    Returns:
        Any | None: Operator object
    """
    oprtrs = []
    rgx: re.Pattern[str] = re.compile(r"same as a (.*) b", flags=re.IGNORECASE)
    for oper_str in op.__dir__():
        try:
            oper = getattr(op, oper_str)
            rgx_match: re.Match[str] | None = rgx.search(oper.__doc__)
            if oper.__module__ == "_operator" and rgx_match:
                grp: str | Any = rgx_match.groups()[0].strip()
                oprtrs += [grp]
                if grp == oprtr:
                    return oper
        except:
            pass
    # return oprtrs    # return oprtrs


def get_cols(table) -> list[str]:
    """Retrieves the column names of an sqlalchemy table class

    Args:
        table (_type_): sqlalchemy table.

    Returns:
        list[str]: List with column names.
    """
    return [col.name for col in table.__table__.c]


async def last_db_entry(table, ses: db.AsyncSession, date_col_str="Date_log") -> str:
    """
    Calculates the time difference of the last added element
    in a table in the format of
    Days - Hours - Minutes - Secs

    Args:
        table (_type_): sqlalchemy table.
        ses (db.AsyncSession): Session object.
        date_col_str (str, optional): Date column name. Defaults to 'Date_log'.

    Returns:
        str: A string of the form: Days - Hours - Minutes - Secs.
    """
    date_col = getattr(table, date_col_str)
    sql = db.select(table).order_by(date_col.desc()).limit(1)
    last_entry = (await ses.execute(sql)).scalar_one()
    td: timedelta = datetime.utcnow() - getattr(last_entry, date_col_str)
    days: int = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} Days - {hours} hours - {minutes} minutes - {seconds}secs"


async def distinct_v_html(field, table, ses: db.AsyncSession) -> str:
    """
    Calculates all the distinct values for a field
    as well as their count for a table.
    The results are returned as html options.

    Args:
        field (_type_): Name of the column.
        table (_type_): Sqlalchemy table.
        ses (db.AsyncSession): Session object.

    Returns:
        str: Html options for the distinct values and their counts.
    """
    col = getattr(table, field)
    sql = (
        db.select(col, db.func.count(col))
        .group_by(col)
        .order_by(db.func.count(col).desc())
    )
    res = (await ses.execute(sql)).all()
    res: list[str] = [f"<option>{x}</option>" for x in res]
    html: str = " ".join(res)
    return html


def process_args(x: str):
    return [x.strip() for x in x.split(",")] if x else []


async def setup_filters(rq_args: dict, table) -> list[BinaryExpression]:
    """
    Constructs column conditions objects
    from a dictionary of arguments of the form


    Args:
        rq_args (dict): Dictionary of arguments of
            the form {column_name: value, column_name_oper: oper_name}.

        table (_type_): Sqlalchemy table.

    Returns:
        _type_: Condition object.
    """
    cols: list[str] = [col.name for col in table.__table__.c]
    rq_cols: dict[str, Any] = {
        k: process_args(v) for k, v in rq_args.items() if k in cols and process_args(v)
    }
    # Iterate through all request args
    log.debug("rq_cols = %s", rq_cols)
    conds: list[BinaryExpression] = []
    for k, v in rq_cols.items():
        log.debug("k = %s, v = %s", k, v)

        # for those columns
        col: Column = getattr(table, k)
        oper_str: str = rq_args[f"{k}_oper"]
        log.debug("oper_str = %s", oper_str)

        # construct condition by applying operators on col objects
        conds.append(setup_filters_oper(v, oper_str, col))  # type: ignore

    log.debug("conds: %s", conds)
    return conds


def setup_filters_oper(v, oper_str: str, col: Column) -> BinaryExpression | None:
    cond = None
    if not oper_str or (oper_str not in db.sa.sql.expression.ColumnElement().__dir__()):
        log.debug("\nOperator: %s not SQLDB", oper_str)
        return cond
    try:
        oper = getattr(col, oper_str)
    except AttributeError:
        try:
            oper = op_func(oper)
        except AttributeError:
            log.error("OPERATOR %s DOES NOT EXIST.", oper)
    else:
        log.debug("oper: %s", oper)
        type_v = col.type.python_type
        log.debug("type_v = %s", type_v)
        trans_v = [eval(x) if type_v is datetime else type_v(x) for x in v]
        log.debug("trans_v = %s", trans_v)

        # operator input tinkering
        try:
            cond = oper(*trans_v)
            log.debug("cond: %s", cond)
        except Exception as e:
            log.error("EXC1 = %s", e)
            try:
                cond = oper(trans_v)
            except Exception as e:
                log.error("IMPLEMENTATION NEEDED FOR INPUT TYPE \nEXC2 = %s", e)
    return cond


async def order_filter(rq_args: dict, table):
    """
    Constructs order_by condition for a given column.

    Args:
        rq_args (dict): Dictionary of arguments of the form
            {column_name: order_by_cols, order_by_mode: mode}.
        table (_type_): Sqlalchemy table

    Returns:
        _type_: Order_by condition object.
    """
    order = None
    if col_str := rq_args.get("order_by_cols"):
        col_str = col_str.strip()
        # log.debug('col_str = %s', col_str)
        col = getattr(table, col_str)
        # log.debug('col = %s', col)
        if mode := rq_args.get("order_by_mode"):
            order = getattr(col, mode)()
        else:
            order = None
        # log.debug('order = %s', order)
    return order


def column_operators() -> list[str]:
    """
    List of all existing Sqlachemy column operators.

    Returns:
        list[str]: List of all existing Sqlachemy column operators in str format.
    """
    return [k for k in ColumnOperators.__dict__.keys() if not k.startswith("_")] + [
        ">=",
        ">",
        "<",
        "<=",
        "==",
    ]


def get_logger_filepath(logger: Logger) -> Path | None:
    if log_paths := [
        handler.baseFilename
        for handler in logger.handlers
        if isinstance(handler, FileHandler)
    ]:
        if (path := Path(next(iter(log_paths)))).exists():
            return path
    return None


async def exec_block(func, /, *args, **kwargs) -> Any:
    loop: AbstractEventLoop = get_running_loop()
    with ThreadPoolExecutor() as pool:
        ctx: Context = copy_context()
        func_call: partial = partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(pool, func_call)


async def exec_processpool(func, /, *args, **kwargs) -> Any:
    loop: AbstractEventLoop = get_running_loop()
    with ProcessPoolExecutor() as pool:
        func_call: partial = partial(func, *args, **kwargs)
        return await loop.run_in_executor(pool, func_call)


def run_async_in_thread(
    loop: asyncio.AbstractEventLoop, coro: Callable[..., Any]
) -> Any:
    """
    This runs the given coroutine in the provided event loop and returns the result.
    """
    return loop.run_until_complete(coro)


async def exec_async_block(func: Callable[..., Any], /, *args, **kwargs) -> Any:
    """
    This runs the given async function in a separate thread and waits for the result.
    """
    loop: AbstractEventLoop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        # Create a new event loop for the new thread
        new_loop: AbstractEventLoop = asyncio.new_event_loop()

        # Prepare the partial function with the new event loop and the given async function
        ctx: Context = copy_context()
        func_call = partial(
            ctx.run, run_async_in_thread, new_loop, func(*args, **kwargs)
        )

        # Run the function in the thread pool and await its result
        result = await loop.run_in_executor(pool, func_call)

        # Close the new event loop
        new_loop.close()

        return result


async def btn_update(
    table,
    rq_args: dict[str, Any],
    btn_type: str,
    ses: db.AsyncSession,
) -> Literal[-1, 0, 1] | None:
    if job_id := rq_args.get("job_id"):
        job = (
            await ses.execute(db.select(table).filter(table.job_id == job_id))
        ).scalar()
        val_old = getattr(job, btn_type)
        # log.debug('val_old: %s', val_old)
        setattr(job, f"{btn_type}", 0 if val_old else 1)
        val_new = getattr(job, btn_type)
        await ses.commit()
        # log.debug('val_new: %s', val_new)
        return val_new
