from logging import Logger

from fastapi import Depends, Request
from fastapi.responses import FileResponse, HTMLResponse
from starlette.templating import _TemplateResponse

from ...config import APISettings, get_api_settings
from ...logger import logdef
from ..utils import check_localhost, render_html
from . import router

log: Logger = logdef(__name__)
config: APISettings = get_api_settings()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(config.FAV_ICON_PATH)
    # return "dummy", 200


@router.get("/", response_class=HTMLResponse)
def main_index(request: Request) -> _TemplateResponse:
    return render_html(
        "index.html",
    )


@router.get("/debug", response_class=HTMLResponse)
def main_index_debug(
    request: Request, dependencies=[Depends(check_localhost)]
) -> _TemplateResponse:
    return render_html(
        "index_debug.html",
    )


@router.get("/api/test", response_class=HTMLResponse)
async def api_test(request: Request):
    return "dummy", 200
