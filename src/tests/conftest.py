import datetime

import pytest
from fastapi.testclient import TestClient

from app import app
from database import Database
from dependencies import auth

Database.testing = True


def override_auth():
    user = {
        "user_id": "test_id",
        "email": "example@test.com",
    }

    return user


app.dependency_overrides[auth.authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
