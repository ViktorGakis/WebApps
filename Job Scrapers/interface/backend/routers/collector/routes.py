from logging import Logger

from fastapi import Request
from fastapi.responses import HTMLResponse

from ...logger import logdef
from ..utils import render_html
from . import router
from starlette.templating import _TemplateResponse
log: Logger = logdef(__name__)


@router.get("/", response_class=HTMLResponse)
def collector_index(request: Request) -> _TemplateResponse:
    return render_html("index.html")
