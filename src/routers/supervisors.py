from fastapi import APIRouter, Depends

from database import Database
from dependencies import auth
from models.user import User

router = APIRouter(prefix="/supervisors", tags=["Supervisors"])


@router.delete(
    "/supervisor/{supervisor_id}", status_code=200, summary="Delete supervisor"
)
async def delete_supervisor(
        supervisor_id: str,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    Elimina un supervisor
    """
    response = await User(db, user).delete_supevisor(supervisor_id)
    return response


@router.delete(
    "/supervised/{supervised_id}", status_code=200, summary="Delete supervised"
)
async def delete_supervised(
        supervised_id: str,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    Elimina un supervisado
    """
    response = await User(db, user).delete_supervised(supervised_id)
    return response


@router.post("/invitation", status_code=200, summary="Accept invitation")
async def accept_invitation(
        code,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    Acepta un código de invitación
    """
    response = await User(db, user).accept_invitation(code)
    return response
