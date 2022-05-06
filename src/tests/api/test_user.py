from starlette.testclient import TestClient
from app import app
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


def test_create_user():
    with TestClient(app) as client:
        body = {
            "first_name": "John",
            "last_name": "Doe",
            "height": 1.70,
            "weight": 67,
            "sex": "M",
            "birth": "2000-02-10",
        }

        # response = client.post("/user/", json=body)
        # assert response.status_code == HTTP_201_CREATED
        # for value in body:
        #     assert body[value] == response.json()[value]
