from logging import Logger
from typing import Any
from starlette.templating import _TemplateResponse
from fastapi import Request
from fastapi.responses import HTMLResponse

from .exec import analytics_gen
from ..utils import jsonResp, parse_body, render_html
from . import router
from ...logger import logdef
from fastapi.responses import JSONResponse
log: Logger = logdef(__name__)


@router.get("/favicon.ico")
def favicon() -> tuple[str, int]:
    return "dummy", 200


@router.get("/", response_class=HTMLResponse)
def main_index(request: Request) -> _TemplateResponse:
    return render_html("index.html")


@router.get("/api/analytics", response_class=HTMLResponse)
async def api_analytics(
    request: Request,
) -> JSONResponse:
    return await analytics_gen(request)