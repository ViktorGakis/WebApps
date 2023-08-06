from fastapi import APIRouter
from .companies import router as r_companies
from .jobs import router as r_jobs

router: APIRouter = APIRouter(
    prefix="/collector",
    tags=["collector"],
    # dependencies=[Depends(get_ses), Depends(get_templates)],    
    responses={404: {"description": "Not found"}},
)

from . import routes

router.include_router(r_jobs)
router.include_router(r_companies)