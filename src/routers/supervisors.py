from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

from database import Database
from dependencies import auth
from schemas.user import UserModel, UserUpdateModel

from utils import generate_code

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


@router.post("/invitation", status_code=200, summary="Accept invitation")
async def accept_invitation(
    code,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    supervisor = await db["user"].find_one({"invitation": code})
    supervised = await db["user"].find_one({"_id": user["user_id"]})

    if supervisor:
        supervisor["invitation"] = generate_code(db)
        supervisor["supervised"].append(supervised["_id"])
        supervised["supervisors"].append(supervisor["_id"])

        await db["user"].update_one({"_id": supervised["_id"]}, {"$set": supervised})
        await db["user"].update_one({"_id": supervisor["_id"]}, {"$set": supervisor})

        return {"status": "ok"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
