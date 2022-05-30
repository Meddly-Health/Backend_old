import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from database import Database
from dependencies import auth
from schemas.user import UserModel, UserUpdateModel

router = APIRouter(prefix="/supervisors", tags=["User"])


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
    supervisor = await db.get_supervisor(supervisor_id)
    supervised = await db.get_supervised(user["user_id"])

    supervised["supervisors"].remove(supervisor_id)
    supervisor["supervised"].remove(user["user_id"])

    await db["user"].update_one({"_id": supervisor_id}, {"$set": supervisor})
    await db["user"].update_one({"_id": user["user_id"]}, {"$set": supervised})

    return {"status": "ok"}


@router.delete(
    "/supervised/{supervised_id}", status_code=200, summary="Delete supervisor"
)
async def delete_supervised(
    supervised_id: str,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Elimina un supervisor
    """
    supervisor = await db.get_supervisor(user["user_id"])
    supervised = await db.get_supervised(supervised_id)

    supervised["supervisors"].remove(user["user_id"])
    supervisor["supervised"].remove(supervised_id)

    await db["user"].update_one({"_id": user["user_id"]}, {"$set": supervisor})
    await db["user"].update_one({"_id": supervised_id}, {"$set": supervised})

    return {"status": "ok"}
