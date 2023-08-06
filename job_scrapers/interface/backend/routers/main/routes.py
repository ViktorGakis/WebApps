from logging import Logger

from fastapi import Request
from fastapi.responses import HTMLResponse
from ..utils import render_html
from ... import db
from . import router
from ...logger import logdef

log: Logger = logdef(__name__)

@router.get("/favicon.ico")
def favicon() -> tuple[str, int]:
    return "dummy", 200


@router.on_event("startup")
async def startup() -> None:
    await db.init()


@router.on_event("shutdown")
async def shutdown() -> None:
    await db.disc()


@router.get("/", response_class=HTMLResponse)
def main_index(request: Request):
    return render_html("index.html")


