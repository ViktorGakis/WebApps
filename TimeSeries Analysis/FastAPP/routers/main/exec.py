import json
from collections import OrderedDict
from logging import Logger
from typing import Optional

from fastapi.responses import JSONResponse
from pandas import DataFrame
from plotly.graph_objects import Figure
from pydantic import BaseModel, Extra, ValidationError, validator

from pipeline.analytics import Stock, StockMetrics, TechDashboard, TechnicalIndicators

from ...logger import logdef
from ..utils import exec_block, jsonify_plotly, jsonResp

log: Logger = logdef(__name__)


class ExecArgs(BaseModel):
    """
    analytics exec vars API
    """

    ticker: str = "GOOG"

    class Config:
        extra: Extra = Extra.forbid

    @validator("*", pre=True)
    def chunk_val(cls, v, field):
        return field.default if (v == "" or v is None) else v


async def parse_exec_args(rq_args) -> ExecArgs | None:
    try:
        return ExecArgs.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())


def generate_analytics(ticker: str) -> JSONResponse:
    stock = Stock(symbol=ticker)
    technicalIndicators = TechnicalIndicators(stock.data, stock.symbol)
    dashboard = TechDashboard(technicalIndicators)
    stock_metrics = StockMetrics(stock.symbol, stock.info)
    plots = dict(technical=dashboard.plot(), fundamental=stock_metrics.create_subplot())
    return jsonResp(OrderedDict({k: jsonify_plotly(v) for k, v in plots.items()}))


async def analytics_gen(
    request,
) -> JSONResponse:
    rq_args: dict[str, str] = dict(request.query_params)
    print(f'{rq_args=}')
    return await exec_block(generate_analytics, **rq_args)
