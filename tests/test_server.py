import pytest

from fastapi.testclient import TestClient
from server import app


client = TestClient(app)

def test_login_success():
    response = client.post("/login", json={"name": "Peter",
                                           "password": "123456"})
    assert response.status_code == 202
    assert response.json() == {"auth_id": "auth_id"}


def test_login_failrue():
    response = client.post("/login", json={"name": "Wrong",
                                           "password": "Wrong"})
    assert response.status_code == 401
    assert response.json() == {"code": 401, "detail": "User is unknow"}


def test_signin_success():
    response = client.post("/signin", json={"name": "NewPeter",
                                            "password": "123456",
                                            "email": "tsar@vseii.rus"})
    assert response.status_code == 201
    assert response.json() == {"code": 201, "detail": "User is created"}


@pytest.mark.skip(reason="Отсутствует функциональность по проверке пользователя.")
def test_signin_failrue():
    response = client.post("/signin", json={"name": "Peter",
                                           "password": "123456",
                                           "email": "tsar@vseii.rus"})
    assert response.status_code == 409
    assert response.json() == {"code": 409, "detail": "Unknow error"}

def test_get_user_success():
    response = client.get("/user", params={"username": "Peter"})
    assert response.status_code == 200
    # assert response.json() == {"code": 200, "detail": "User is created"}


def test_post_user_sucess():
    response = client.post("/user", json={"name": "PeterTheOne",
                                          "login": "peter_the_one",
                                          "password": "123456",
                                          "email": "peter@theone.rus",
                                          "is_deleted": False,
                                          "is_activated": True})
    assert response.status_code == 201
    assert response.json() == {"name": "PeterTheOne",
                               "login": "peter_the_one",
                               "email": "peter@theone.rus",
                               "is_deleted": False,
                               "is_activated": True}


@pytest.mark.skip(reason="Отсутствует функциональность по проверке пользователя.")
def test_post_user_failrue():
    response = client.post("/user", json={"name": "Peter",
                                          "login": "peter_the_new",
                                          "password": "123456",
                                          "email": "peter@tsar.rus",
                                          "is_deleted": False,
                                          "is_activated": True,
                                          "auth_id": "auth_id"})
    assert response.status_code == 200
