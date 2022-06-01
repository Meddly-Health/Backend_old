import datetime

import firebase_admin
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

import config
from database import Database
from utils import generate_code

cred = credentials.Certificate(config.firebase)
firebase_admin.initialize_app(cred)


async def authenticate(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db=Depends(Database.get_db),
):
    """
    Authenticate a user with a Bearer token.
    This does not support the supervisor role.
    """

    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
        )

    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
        )

    user = await db["user"].find_one({"_id": decoded_token["user_id"]})
    if not user:
        user = {
            "_id": decoded_token["user_id"],
            "email": decoded_token["email"],
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "diseases": [],
            "supervisors": [],
            "supervised": [],
            "invitation": await generate_code(db),
        }
        await db["user"].insert_one(user)
    return {"user_id": decoded_token["user_id"], "email": decoded_token["email"]}


async def authenticate_with_supervisor(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db=Depends(Database.get_db),
    supervised_id: str | None = Header(default=None),
):
    """
    Authenticate a user with a Bearer token.
    This supports the supervisor role.
    """
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
        )

    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
        )

    if supervised_id:
        user = await db["user"].find_one({"_id": supervised_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Supervised user does not exist",
            )
        if decoded_token["user_id"] not in user["supervisors"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not a supervisor of the supervised user",
            )
        return {"user_id": user["user_id"], "email": user["email"]}

    user = await db["user"].find_one({"_id": decoded_token["user_id"]})
    if not user:
        user = {
            "_id": decoded_token["user_id"],
            "email": decoded_token["email"],
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "diseases": [],
            "supervisors": [],
            "supervised": [],
            "invitation": await generate_code(db),
        }
        await db["user"].insert_one(user)
    return {"user_id": user["user_id"], "email": user["email"]}
