from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/locator",
    tags=["locator"],
    # dependencies=[Depends(get_ses), Depends(get_templates)],    
    responses={404: {"description": "Not found"}},
)

from . import routes