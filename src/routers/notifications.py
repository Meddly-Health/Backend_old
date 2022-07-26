from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from database import Database
from dependencies import auth

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", status_code=200, summary="Update notification preferences")
async def update_notification_preferences(
    notifications: list[str],
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Actualiza la preferencia del usuario para recibir las notificaciones (sobreecribiendo el objeto completo):

    - **active_notifications**
    """

    notifications = jsonable_encoder(notifications)

    await db["user"].update_one(
        {"_id": user["user_id"]},
        {"$set": {f"active_notifications": notifications}},
    )
    return {"status": "ok"}


