import operator as op
import re
from datetime import datetime
from logging import Logger
from typing import Any
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import Column
from sqlalchemy.sql.expression import ColumnOperators

from .. import db
from ..config import APISettings, get_api_settings
from ..db.models import Job
from ..logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


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


def process_args(x: str):
    return [x.strip() for x in x.split(",")] if x else []


class DbConditions:
    def __init__(self, rq_args: dict[str, str], table):
        self.rq_args: dict[str, str] = rq_args
        self.table = table
        self.conds: list[BinaryExpression] = []
        self.cols: list[str] = [col.name for col in table.__table__.c]
        self.__rq_cols()
    
    
    def __rq_cols(self) -> None:
        self.rq_cols: dict[str, list[str]] = {
                k: process_args(v) 
                for k, v in self.rq_args.items() 
                if k in self.cols and process_args(v)
            }   
        log.debug("self.rq_cols = %s", self.rq_cols)     


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

        # construct conditions by applying operators on col objects
        conds: list[BinaryExpression] = setup_filters_oper(oper_str, col)
        
    log.debug("conds: %s", conds)
    return conds


def setup_filters_oper(oper_str: str, col: Column) -> list[BinaryExpression]:
    conds: list[BinaryExpression] = []
    if (
        not oper_str
        or oper_str not in db.sa.sql.expression.ColumnElement().__dir__()
    ):
        return conds
    
    oper, trans_v = setup_filters_oper_prepare(col, oper_str)

        # operator input tinkering
    conds = setup_filters_oper_apply(trans_v, conds)
    return conds

def setup_filters_oper_prepare(col, oper_str):
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
        return oper, trans_v

def setup_filters_oper_apply(trans_v, conds):
    try:
        cond = oper(*trans_v)
    except Exception as e:
        log.error("EXC1 = %s", e)
        try:
            cond = oper(trans_v)
        except Exception as e:
            log.error("IMPLEMENTATION NEEDED FOR INPUT TYPE \nEXC2 = %s", e)
        else:
            conds += [cond]
    else:
        log.debug("cond: %s", cond)
        conds += [cond]   
    return conds

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


