from collections import OrderedDict
from logging import Logger
from typing import Any, Dict, List

from fastapi.responses import JSONResponse
from pandas import DataFrame
from pydantic import BaseModel, Extra, Field, ValidationError, validator

from pipeline.analytics import Stock, StockMetrics, TechDashboard, TechnicalIndicators
from pipeline.predictions.models.elasticnet import ElasticNetRegressor, ElasticNetParams
from pipeline.predictions.preprocess.preprocess import DataPreparer

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


async def parse_exec_args(rq_args, pydantic_model) -> ExecArgs | None:
    try:
        return ExecArgs.parse_obj(rq_args)
    except ValidationError as e:
        log.error("%s", e.json())


def generate_analytics(ticker: str) -> JSONResponse | str:
    stock = Stock(symbol=ticker)
    if isinstance(stock.data, DataFrame) and stock.data.shape[0] > 0:
        technicalIndicators = TechnicalIndicators(stock.data, stock.symbol)
        dashboard = TechDashboard(technicalIndicators)
        stock_metrics = StockMetrics(stock.symbol, stock.info)
        plots = dict(
            technical=dashboard.plot(), fundamental=stock_metrics.create_subplot()
        )
        return jsonResp(OrderedDict({k: jsonify_plotly(v) for k, v in plots.items()}))
    else:
        return jsonResp({"data": "Hello, World!"})


async def analytics_gen(
    ticker: str,
) -> JSONResponse:
    return await exec_block(generate_analytics, ticker)


class ExecArgsDataPrep(BaseModel):
    target_column: str = "Close"
    test_size: float = 0.2

    class Config:
        extra: Extra = Extra.forbid

    @validator("*", pre=True)
    def chunk_val(cls, v, field):
        return field.default if (v == "" or v is None) else v


def data_prep_gen(ticker, target_column, test_size) -> JSONResponse:
    stock = Stock(symbol=ticker)
    dp = DataPreparer(stock.data, target_column, test_size)
    return jsonResp(OrderedDict({"Data Preparer": jsonify_plotly(dp)}))


class ElasticNetParameters(BaseModel):
    # ticker: str = Field(..., title="Ticker")
    # target_col: str = Field(..., title="Target Column")
    # test_size: float = Field(0.2, title="Test Size")
    cv: int = Field(5, title="CV")
    threshold: float = Field(0.2, title="Threshold")
    alpha: List[float] = Field([0.001, 0.01, 0.1, 1, 10, 100], title="Alpha")
    l1_ratio: List[float] = Field([0.1, 0.3, 0.5, 0.7, 0.9], title="L1 Ratio")
    max_iter: List[int] = Field([1000, 2000, 5000], title="Max Iterations")
    tol: List[float] = Field([1e-4, 1e-5, 1e-6], title="Tolerance")
    selection: List[str] = Field(["cyclic", "random"], title="Selection")

    class Config:
        extra: Extra = Extra.forbid

    @validator("*", pre=True)
    def chunk_values(cls, v, field):
        if v == "" or v is None:
            return field.default

        key = field.name
        try:
            if key in {"ticker", "target_col"}:
                return v
            elif key in {"threshold", "test_size"}:
                return float(v)
            elif key in {"cv"}:
                return int(v)
            elif key == "selection":
                return v.split(",")
            elif "," in str(v):
                return [float(value) for value in str(v).split(",") if value]
            else:
                return [float(v)]
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid values for parameter '{key}'. Expected float or comma-separated floats."
            )


def parse_params_elasticnet(request) -> Dict[str, Any] | None:
    parameters: dict[str, str] = {
        # "ticker": request.query_params.get("ticker"),
        # "target_col": request.query_params.get("target_col"),
        # "test_size": request.query_params.get("test_size"),
        "cv": request.query_params.get("cv"),
        "threshold": request.query_params.get("threshold"),
        "alpha": request.query_params.get("alpha"),
        "l1_ratio": request.query_params.get("l1_ratio"),
        "max_iter": request.query_params.get("max_iter"),
        "tol": request.query_params.get("tol"),
        "selection": request.query_params.get("selection"),
    }

    try:
        return ElasticNetParameters(**parameters).dict()
    except ValidationError as e:
        log.error("%s", e.json())


def elasticnet_exec(request):
    params: Dict[str, Any] | None = parse_params_elasticnet(request)
    print("params:::", params)
    ticker = params.get("ticker")
    target_col = params.get("target_col")
    test_size = params.get("test_size")
    cv = params.get("cv")
    threshold = params.get("threshold")
    print("params", params)
    stock = Stock(symbol=ticker)
    dp = DataPreparer(stock.data, target_col, test_size)
    regressor = ElasticNetRegressor(dp)
    param_grid = {
        key: params[key]
        for key in [
            "alpha",
            "l1_ratio",
            "max_iter",
            "tol",
            "selection",
        ]
    }
    # Perform tuning and evaluation
    regressor.gridcv_tune(param_grid, cv=cv)

    return dict(
        summary=regressor.summarize(threshold),
        plot_predictions=regressor.plot(),
        plot_learning_curve=regressor.plot_learning_curve(),
    )
