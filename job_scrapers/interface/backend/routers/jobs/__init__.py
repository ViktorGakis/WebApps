from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    # dependencies=[Depends(get_ses), Depends(get_templates)],    
    responses={404: {"description": "Not found"}},
)

from . import routes
