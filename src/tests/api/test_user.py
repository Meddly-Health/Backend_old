from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from starlette.testclient import TestClient

body = {
    "first_name": "John",
    "last_name": "Doe",
    "height": 1.70,
    "weight": 67,
    "sex": "M",
    "birth": "2000-02-10T00:00:00+00:00",
}


def test_create_user(client: TestClient):
    response = client.post("/user/", headers={"cred": "test"}, json=body)
    assert response.status_code == HTTP_201_CREATED
    for value in body:
        assert body[value] == response.json()[value]


def test_get_user(client: TestClient):
    response = client.get("/user/", headers={"cred": "test"})
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]


def test_update_user(client: TestClient):
    new_sex = "F"
    body["sex"] = new_sex
    response = client.patch("/user/", headers={"cred": "test"}, json={"sex": new_sex})
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]


def test_delete_user(client: TestClient):
    response = client.delete("/user/", headers={"cred": "test"})
    assert response.status_code == HTTP_200_OK
