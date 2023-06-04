from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="",
)

from . import routes