import pytest
from fastapi.testclient import TestClient

from app import app
from database import Database
from dependencies import auth


def override_auth():
    user = {
        "user_id": "test_id",
        "email": "example@test.com",
        "email_verified": False,
        "firebase": {
            "identities": {"email": ["test@test.com"]},
            "sign_in_provider": "password",
        },
        "uid": "test_id",
    }
    return user


app.dependency_overrides[auth.authenticate] = override_auth

Database.testing = True


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
