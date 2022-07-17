import pytest

from fastapi.testclient import TestClient
from server import app


client = TestClient(app)


class TestMainPage:
    def test_main_page(self):
        response = client.get("/", params={"skip": 1, "limit": 100})
        assert response.status_code == 200

    def test_main_page_failrue(self):
        response = client.get("/", params={"skip": 1, "limit": 101})
        assert response.status_code == 406


class TestLogin:
    def test_login_success(self):
        response = client.post("/auth/login",
                               json={"name": "Peter",
                                     "password": "123456"})
        assert response.status_code == 202
        assert response.json() == {"auth_id": "auth_id"}

    def test_login_failrue(self):
        response = client.post("/auth/login",
                               json={"name": "Wrong",
                                     "password": "Wrong"})
        assert response.status_code == 401
        assert response.json() == {"code": 401, "detail": "User is unknow"}


class TestSignin:
    def test_signin_success(self):
        response = client.post("/auth/signin",
                               json={"name": "NewPeter",
                                     "password": "123456",
                                     "email": "tsar@vseii.rus"})
        assert response.status_code == 201
        assert response.json() == {"code": 201, "detail": "User is created"}

    @pytest.mark.skip(reason="Отсутствует функциональность.")
    def test_signin_failrue():
        response = client.post("/auth/signin",
                               json={"name": "Peter",
                                     "password": "123456",
                                     "email": "tsar@vseii.rus"})
        assert response.status_code == 409
        assert response.json() == {"code": 409, "detail": "Unknow error"}


class TestAdminPanel:
    def test_get_user_success(self):
        response = client.get("/admin/user", params={"username": "Peter"})
        assert response.status_code == 200
        # assert response.json() == {"code": 200, "detail": "User is created"}

    def test_post_user_sucess(self):
        response = client.post("/admin/user",
                               json={"name": "PeterTheOne",
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

    @pytest.mark.skip(reason="Отсутствует функциональность.")
    def test_post_user_failrue(self):
        response = client.post("/admin/user", json={"name": "Peter",
                                                    "login": "peter_the_new",
                                                    "password": "123456",
                                                    "email": "peter@tsar.rus",
                                                    "is_deleted": False,
                                                    "is_activated": True,
                                                    "auth_id": "auth_id"})
        assert response.status_code == 200
