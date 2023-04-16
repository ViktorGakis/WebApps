from logging import Logger
from starlette.templating import _TemplateResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from ..utils import render_html
from . import router
from ...logger import logdef

log: Logger = logdef(__name__)

@router.get("/favicon.ico")
def favicon() -> tuple[str, int]:
    return "dummy", 200


@router.get("/", response_class=HTMLResponse)
def main_index(request: Request) -> _TemplateResponse:
    return render_html("index.html")


