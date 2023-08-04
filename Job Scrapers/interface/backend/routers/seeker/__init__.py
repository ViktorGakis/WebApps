from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/seeker",
    tags=["seeker"],
    # dependencies=[Depends(get_ses), Depends(get_templates)],    
    responses={404: {"description": "Not found"}},
)

from . import routes
