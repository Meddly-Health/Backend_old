import datetime

import pytest
from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

from app import app
from database import Database
from dependencies import auth
from models.user import User

Database.testing = True


async def override_auth(cred: str = Header(default=None), db=Depends(Database.get_db)):
    credentials = {'user_id': cred, 'email': f"{cred}@test.com"}
    await User(db, credentials).assert_user()
    return credentials


app.dependency_overrides[auth.authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
