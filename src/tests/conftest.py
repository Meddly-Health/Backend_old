import datetime

import pytest
from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

from app import app
from database import Database
from dependencies import auth
from utils import generate_code

Database.testing = True


async def override_auth(cred: str = Header(default=None),
                        db=Depends(Database.get_db)):
    user = await db["user"].find_one({"_id": cred})
    if not user:
        user = {
            "_id": cred,
            "email": f"{cred}@test.com",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "diseases": [],
            "supervisors": [],
            "supervised": [],
            "invitation": await generate_code(db),
        }
        await db["user"].insert_one(user)
    return {"user_id": cred, "email": f"{cred}@test.com"}


app.dependency_overrides[auth.authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
