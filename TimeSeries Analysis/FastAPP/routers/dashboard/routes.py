from logging import Logger

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from ...logger import logdef
from ..utils import render_html
from . import router

log: Logger = logdef(__name__)


@router.get("/favicon.ico")
def favicon() -> tuple[str, int]:
    return "dummy", 200


@router.get("/", response_class=HTMLResponse)
def dashboard_index(request: Request) -> _TemplateResponse:
    return render_html("dashboard/index.html")
