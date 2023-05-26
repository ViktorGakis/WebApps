from logging import Logger
from pprint import pprint
from typing import Any, List
from pydantic import ValidationError
from starlette.templating import _TemplateResponse
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse

from .exec import ElasticNetParameters, ElasticNetParams, analytics_gen, elasticnet_exec
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
        {"ElasticNetParams":ElasticNetParams}
    )


@router.get("/api/analytics", response_class=HTMLResponse)
async def api_analytics(
    request: Request,
    ticker: CurrentTicker = Depends(get_my_ticker)
) -> JSONResponse:
    if val:=request.query_params.get('ticker'):
        ticker.value = val
    return await analytics_gen(ticker.value)


@router.get("/api/preprocess", response_class=HTMLResponse)
async def api_preprocess(
    request: Request,
    ticker: CurrentTicker = Depends(get_my_ticker)
) -> JSONResponse:
    if val:=request.query_params.get('ticker'):
        ticker.value = val
    
    return preprocess_gen(ticker.value, target_column, test_size)


@router.get("/api/test", response_class=HTMLResponse)
async def api_test(
    request: Request,
    ticker: CurrentTicker = Depends(get_my_ticker)
) -> JSONResponse:
    if val:=request.query_params.get('ticker'):
        ticker.value = val
    return jsonResp({"ticker": ticker.value})


@router.get("/api/models/elasticnet")
async def api_models_elasticnet(request: Request):
    params = request.query_params._dict
    pprint(request.query_params._dict)
    checked_params = {k:v for k,v in params.items() if k.endswith("_checked")}
    pprint(checked_params)
    cleaned_params = {
        k.replace('_checked','').replace("_user_input","").replace("_default","").replace("_grid_values",""):v 
        for k,v in checked_params.items()
    }
    pprint(cleaned_params)
    try:
        params = ElasticNetParameters(**cleaned_params).dict()
        pprint(params)
    except ValidationError as e:
        log.error("%s", e.json())
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
    pprint(param_grid)        
    return 'okboi'
    # return await exec_block(elasticnet_exec, request)



