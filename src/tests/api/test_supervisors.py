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


def test_accept_invitation(client: TestClient):
    # Primero creamos 3 usuarios que van a servir para la prueba
    test_user = client.post("/user/", headers={"cred": "test"}, json=body).json()
    supervisor_user = client.post("/user/", headers={"cred": "supervisor"}, json=body).json()
    supervised_user = client.post("/user/", headers={"cred": "supervised"}, json=body).json()

    # Aceptamos las invitaciones
    # Acá, test acepta la invitación de supervisor
    test1_response = client.post(f"/supervisors/invitation?code={supervisor_user['invitation']}",
                                 headers={"cred": "test"})
    # Acá, el supervisado acepta la invitación de test
    test2_response = client.post(f"/supervisors/invitation?code={test_user['invitation']}",
                                 headers={"cred": "supervised"})

    # Comprobamos Status codes
    assert test1_response.status_code == HTTP_200_OK
    assert test2_response.status_code == HTTP_200_OK

    # Comprobamos que ambos usuarios están en la lista de supervisores y supervisados
    test_user = client.get("/user/", headers={"cred": "test"}).json()
    supervisor_user = client.get("/user/", headers={"cred": "supervisor"}).json()
    supervised_user = client.get("/user/", headers={"cred": "supervised"}).json()

    assert test_user['supervised'][0]['_id'] == supervised_user['_id']
    assert test_user['supervisors'][0]['_id'] == supervisor_user['_id']
    assert supervised_user['supervisors'][0]['_id'] == test_user['_id']
    assert supervisor_user['supervised'][0]['_id'] == test_user['_id']

    assert len(test_user['supervised']) == 1
    assert len(test_user['supervisors']) == 1
    assert len(supervised_user['supervisors']) == 1
    assert len(supervisor_user['supervised']) == 1


def test_delete_supervisor(client: TestClient):
    test_user = client.get("/user/", headers={"cred": "test"}).json()
    supervisor_user = client.get("/user/", headers={"cred": "supervisor"}).json()

    response = client.delete(f"/supervisors/supervisor/{supervisor_user['_id']}", headers={"cred": "test"})

    assert response.status_code == HTTP_200_OK

    test_user = client.get("/user/", headers={"cred": "test"}).json()
    supervisor_user = client.get("/user/", headers={"cred": "supervisor"}).json()

    assert len(test_user['supervisors']) == 0
    assert len(supervisor_user['supervised']) == 0


def test_delete_supervised(client: TestClient):
    test_user = client.get("/user/", headers={"cred": "test"}).json()
    supervised_user = client.get("/user/", headers={"cred": "supervised"}).json()

    response = client.delete(f"/supervisors/supervised/{supervised_user['_id']}", headers={"cred": "test"})

    assert response.status_code == HTTP_200_OK

    test_user = client.get("/user/", headers={"cred": "test"}).json()
    supervised_user = client.get("/user/", headers={"cred": "supervised"}).json()

    assert len(test_user['supervised']) == 0
    assert len(supervised_user['supervisors']) == 0
