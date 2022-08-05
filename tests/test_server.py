from fastapi import Response
import pytest
from unittest.mock import patch
from unittest.mock import Mock

from fastapi.testclient import TestClient

from server import app
from src.db.worker import DBWorker
from src.routers.admin_panel import add_user, userlist
from src.schemas.schemas import Token, UserLogin
from src.routers.auth import login
from src.core.deps import check_auth_token


def fake_depends() -> None:
    return None


app.dependency_overrides[check_auth_token] = fake_depends
client = TestClient(app)


class TestMainPage:
    def test_success(self):
        response = client.get("/", params={"skip": 1, "limit": 100})
        assert response.status_code == 200

    def test_failrue(self):
        response = client.get("/", params={"skip": 1, "limit": 101})
        assert response.status_code == 406


class TestLogin:
    def test_success(self, fx_db):
        response = client.post("/auth/login",
                               json={"name": "Test",
                                     "password": "Test"})
        assert response.status_code == 202

    @patch('src.routers.auth.check_password', return_value=False)
    def test_failrue(self, mock_check_pass, fx_db):
        response = client.post("/auth/login",
                               json={"name": "Test2",
                                     "password": "Test2"})
        assert mock_check_pass.call_count == 1
        assert response.status_code == 401
        assert response.json() == {"code": 401,
                                   "detail": "User is unknow"}

    @pytest.mark.asyncio
    @patch.object(DBWorker, 'get_user', spec=UserLogin)
    @patch('src.routers.auth.check_password', return_value=True)
    async def test_unit_success(self, mock_password, _, fx_user):
        mock_response = Mock(spec=Response)
        result = await login(user=fx_user, response=mock_response)
        assert mock_password.call_count == 1
        assert isinstance(result.auth_id, str)

    @pytest.mark.asyncio
    @patch.object(DBWorker, 'get_user', spec=UserLogin)
    @patch('src.routers.auth.check_password', return_value=False)
    async def test_unit_error(self, mock_password, _, fx_user):
        mock_response = Mock(spec=Response)
        result = await login(user=fx_user, response=mock_response)
        assert mock_password.call_count == 1
        assert result.code == 401


class TestSignin:
    def test_success(self, fx_db):
        response = client.post("/auth/signin",
                               json={"name": "NewPeter",
                                     "password": "123456",
                                     "email": "tsar@vseii.rus"})
        assert response.status_code == 201
        assert response.json() == {"code": 201, "detail": "User is created"}

    @patch.object(DBWorker, 'add_user', side_effect=Exception('Err'))
    def test_failrue(self, mock_add_user):
        response = client.post("/auth/signin",
                               json={"name": "Peter",
                                     "password": "123456",
                                     "email": "tsar@vseii.rus"})
        assert mock_add_user.call_count == 1
        assert response.status_code == 409
        assert response.json() == {"code": 409, "detail": "Unknow error"}


class TestAdminPanel:
    class TestGetUser:
        @pytest.mark.asyncio
        @patch.object(DBWorker,
                      'get_user',
                      spec=UserLogin,
                      return_value=UserLogin(name="Test"))
        async def test_unit_userlist(self, mock_db):
            mock_response = Mock(spec=Response)
            result = await userlist(response=mock_response, username="Test")
            assert result.name == "Test"

        def test_success(self,
                         fx_headers,
                         fx_db):
            response = client.get("/admin/user",
                                  params={"username": "Test"},
                                  headers=fx_headers)
            assert response.status_code == 200

        def test_failrue(self):
            response = client.get("/admin/user",
                                  params={"username": "Peter"},
                                  headers={"token": "wrong"})
            assert response.status_code == 404

    class TestPostUser:
        @pytest.mark.asyncio
        @patch.object(DBWorker, 'add_user')
        async def test_unit_add_user(self, mock_db, fx_user_create):
            mock_response = Mock(spec=Response)
            result = await add_user(item=fx_user_create,
                                    response=mock_response)
            assert result.name == "PeterTheTwo"

        def test_sucess(self, fx_headers, fx_json):
            response = client.post("/admin/user",
                                   json=fx_json,
                                   headers=fx_headers)
            assert response.status_code == 201
            assert response.json() == {"name": "PeterTheOne",
                                       "login": "peter_the_one",
                                       "email": "peter@theone.rus",
                                       "is_deleted": False,
                                       "is_activated": True}

        @patch.object(DBWorker, 'add_user', side_effect=KeyError())
        def test_failrue(self, _, fx_json):
            response = client.post("/admin/user",
                                   json=fx_json)
            assert response.status_code == 500


class TestToken:
    @pytest.mark.skip("Not working")
    def test_sucess(self, _, fx_db):
        result = client.post("/auth/token",
                             data={"username": "Test",
                                   "password": "Test"})
        assert result is Token

    @pytest.mark.skip("Not working")
    def test_failrue(self, _, fx_db):
        result = client.post("/auth/token",
                             data={"username": "Test",
                                   "password": "Test"})
        assert result is Token
