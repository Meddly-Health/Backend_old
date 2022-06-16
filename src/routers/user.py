import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from database import Database
from dependencies import auth
from models.user import User
from schemas.user import UserModel, UserUpdateModel

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=UserModel, status_code=200, summary="Get user data")
async def get_user(user=Depends(auth.authenticate), db=Depends(Database.get_db)):
    """
    Obtener la información de un usuario
    """

    return await User.get(db, user)


@router.post("/", response_model=UserModel, status_code=200, summary="Update user data")
async def update_user(
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
    - **avatar**
    """

    return await User.update(db, user, user_data)


@router.delete("/", status_code=200, summary="Delete user")
async def delete_user(
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Elimina completamente a un usuario
    """

    return await User.delete(db, user)
