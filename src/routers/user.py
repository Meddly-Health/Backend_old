import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from database import Database
from dependencies import auth
from schemas.user import UserModel, UserUpdateModel

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", status_code=200, summary="Get user data")
async def get_user(user=Depends(auth.authenticate), db=Depends(Database.get_db)):
    """
    Obtener la información de un usuario
    """
    # user = await db["user"].find_one({"user_id": user["user_id"]})
    pipeline = [
        {"$match": {"user_id": user["user_id"]}},
        {'$lookup': {
            'from': 'user',
            "localField": "supervised",
            "foreignField": "_id",
            "as": "supervised",
            "pipeline": [
                {"$project": {"email": 1, "_id": 0}},
            ]
        }}
    ]
    a = (await db["user"].aggregate(pipeline).to_list(length=1))[0]
    print(a)

    return {}


@router.post("/", response_model=UserModel, status_code=201, summary="Update user data")
async def create_user(
        user_data: UserUpdateModel,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    Actualiza los datos de un usuario (sobreecribiendo el objeto completo):

    - **first_name**
    - **last_name**
    - **height**
    - **weight**
    - **sex**
    - **birth**
    """
    old_created_date = await db["user"].find_one(
        {"user_id": user["user_id"]}, {"_id": 0}
    )
    old_created_date = old_created_date["created_at"]

    user_data = jsonable_encoder(user_data)
    new_user = {
        "user_id": user["user_id"],
        "email": user["email"],
        "created_at": old_created_date,
        "updated_at": datetime.datetime.now(),
        "diseases": [],
        "supervisors": [],
        "supervised": [],
    }

    for data in user_data:
        if user_data[data] is not None:
            new_user[data] = user_data[data]

    await db["user"].update_one({"user_id": user["user_id"]}, {"$set": new_user})
    return new_user


@router.patch(
    "/", response_model=UserModel, status_code=200, summary="Update user data"
)
async def update_user(
        user_data: UserUpdateModel,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    Actualiza los datos de un usuario (sin sobreescribirlos):

    - **first_name**
    - **last_name**
    - **height**
    - **weight**
    - **sex**
    - **birth**
    """

    new_user = await db["user"].find_one({"user_id": user["user_id"]}, {"_id": 0})

    new_user_data = jsonable_encoder(user_data)

    for data in new_user_data:
        if new_user_data[data] is not None:
            new_user[data] = new_user_data[data]

    new_user["updated_at"] = datetime.datetime.now()

    await db["user"].update_one({"user_id": user["user_id"]}, {"$set": new_user})
    return new_user


@router.delete("/", status_code=200, summary="Delete user")
async def delete_user(
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    Elimina completamente a un usuario
    """
    # TODO: Eliminar todos los datos del usuario (y sus relaciones)

    await db["user"].delete_one({"user_id": user["user_id"]})
    return {"status": "ok"}
