from fastapi import APIRouter, Depends

from database import Database
from dependencies import auth
from models.user import User

router = APIRouter(prefix="/programaciones", tags=["Supervisors"])


@router.delete(
    "/supervisor/{supervisor_id}", status_code=200, summary="Delete supervisor"
)
async def delete_supervisor(
    supervisor_id: str,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    pass
