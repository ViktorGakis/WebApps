from logging import Logger
from pprint import pprint
from typing import Any, List
from pydantic import ValidationError
from starlette.templating import _TemplateResponse
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse

from pipeline.predictions import PreprocessParams, ElasticNetParams


from .exec import ElasticNetParameters, analytics_gen, data_prep_exec, elasticnet_exec
from ..utils import exec_block, jsonResp, parse_body, render_html
from . import router
from ...logger import logdef
from fastapi.responses import JSONResponse

log: Logger = logdef(__name__)


class CurrentTicker:
    def __init__(self) -> None:
        self.value = None


current_ticker = CurrentTicker()


def get_my_ticker() -> CurrentTicker:
    return current_ticker


@router.get("/favicon.ico")
def favicon() -> tuple[str, int]:
    return "dummy", 200


@router.get("/", response_class=HTMLResponse)
def main_index(request: Request) -> _TemplateResponse:
    return render_html(
        "index.html",
        {"ElasticNetParams": ElasticNetParams, "PreprocessParams": PreprocessParams},
    )


@router.get("/api/analytics", response_class=HTMLResponse)
async def api_analytics(
    request: Request, ticker: CurrentTicker = Depends(get_my_ticker)
) -> JSONResponse:
    if val := request.query_params.get("ticker"):
        ticker.value = val
    return await analytics_gen(ticker.value)


@router.get("/api/preprocess", response_class=HTMLResponse)
async def api_preprocess(
    request: Request, ticker: CurrentTicker = Depends(get_my_ticker)
) -> JSONResponse:
 
    # if val := request.query_params.get("ticker"):
    #     ticker.value = val

    # return preprocess_gen(ticker.value, target_column, test_size)
    return await data_prep_exec(request)

@router.get("/api/test", response_class=HTMLResponse)
async def api_test(
    request: Request, ticker: CurrentTicker = Depends(get_my_ticker)
) -> JSONResponse:
    return "<p><strong>TEST</strong></p><p> url_for('api_models_elasticnet') </p>"
    return JSONResponse(content={"ticker": "GOOG"})
    return jsonResp({"ticker": "GOOG"})


@router.get("/api/models/elasticnet")
async def api_models_elasticnet(request: Request):

    return await exec_block(elasticnet_exec, request)
