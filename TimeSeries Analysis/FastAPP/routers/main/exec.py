from collections import OrderedDict
from logging import Logger
from typing import Any, Dict, List

from fastapi.responses import JSONResponse
from pandas import DataFrame
from pydantic import BaseModel, Extra, Field, ValidationError, validator

from pipeline.analytics import Stock, StockMetrics, TechDashboard, TechnicalIndicators
from pipeline.predictions import ElasticNetRegressor, ElasticNetParams
from pipeline.predictions.preprocess.preprocess import DataPreparer

from ...logger import logdef
from ..utils import exec_block, jsonify_plotly, jsonResp, save_object

log: Logger = logdef(__name__)

stock = None
dp = None


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
    global stock
    stock = Stock(symbol=ticker)
    # save_object(stock, 'data/stock.joblib')
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
    ticker: str = Field(..., title="Ticker")
    target_col: str = Field(..., title="Target Column")
    test_size: float = Field(0.2, title="Test Size")

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
            elif key in {"test_size"}:
                return float(v)
            elif "," in str(v):
                return [float(value) for value in str(v).split(",") if value]
            else:
                return [float(v)]
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid values for parameter '{key}'. Expected float or comma-separated floats."
            )


def first_param_parse(request):
    q_params = request.query_params._dict
    # print(request.query_params._dict)
    checked_params = {k: v for k, v in q_params.items() if k.endswith("_checked")}
    # print(checked_params)
    return {
        k.replace("_checked", "")
        .replace("_user_input", "")
        .replace("_default", "")
        .replace("_grid_values", ""): v
        for k, v in checked_params.items()
    }


def data_prep(request) -> JSONResponse:
    global dp_params, stock, dp
    cleaned_params = first_param_parse(request)
    # print(cleaned_params)
    dp_params = ExecArgsDataPrep(**cleaned_params).dict()
    if stock is None:
        stock = Stock(symbol=dp_params["ticker"])
    dp = DataPreparer(stock.data, dp_params["target_col"], dp_params["test_size"])
    save_object(dp, "data/dp.joblib")
    return jsonResp(
        OrderedDict(
            {
                # "stock_data": dp.data.to_html(classes="table table-dark table-striped"),
                # "X": dp.X.to_html(classes="table table-dark table-striped"),
                # "y": dp.y.to_html(classes="table table-dark table-striped"),
                # "X_train": dp.X_train.to_html(classes="table table-dark table-striped"),
                # "y_train": dp.y_train.to_html(classes="table table-dark table-striped"),
                # "X_test": dp.X_test.to_html(classes="table table-dark table-striped"),
                # "y_test": dp.y_test.to_html(classes="table table-dark table-striped"),
                "plot": jsonify_plotly(dp.plot()),
            }
        )
    )


async def data_prep_exec(request) -> JSONResponse:
    return await exec_block(data_prep, request)


class ElasticNetParameters(BaseModel):
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
            elif key in {"alpha", "l1_ratio"}:
                return [float(value) for value in v.replace("[", "").replace("]", "").split(",") if value.strip()]
            else:
                return [float(v)]
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid values for parameter '{key}'. Expected float or comma-separated floats."
            )


def parse_params_elasticnet(request) -> Dict[str, Any] | None:
    cleaned_params = first_param_parse(request)
    print(cleaned_params)
    try:
        return ElasticNetParameters(**cleaned_params).dict()
    except ValidationError as e:
        log.error("%s", e.json())


def elasticnet_exec(request):
    global dp, stock, dp_params

    params: Dict[str, Any] | None = parse_params_elasticnet(request)
    print("params", params)
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
    print("param_grid", param_grid)
    if dp is None:
        return jsonResp(
            {
                "error": "No Data Prepared Available. Please Prepare the data in Preprocess.",
            }
        )
    regressor = ElasticNetRegressor(dp)
    # Perform tuning and evaluation
    regressor.gridcv_tune(param_grid, cv=params["cv"])
    regressor.calculate_learning_curve()
    regressor.calculate_optimal_size()

    return jsonResp(
        dict(
            summary_pre=regressor.summarize(params["threshold"]),
            plot_predictions_plotly=jsonify_plotly(regressor.plot()),
            plot_learning_curve_plotly=jsonify_plotly(regressor.plot_learning_curve()),
        )
    )
