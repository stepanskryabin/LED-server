from unittest.mock import patch
from jose import jwt

from passlib.context import CryptContext

from src.core.security import verify_password
from src.core.security import get_password_hash
from src.core.security import authenticate_user
from src.core.security import create_access_token
from src.db.worker import DBWorker


class TestAccessToken:
    @patch.object(jwt, 'encode')
    def test_create_access_token(self, mock_encode):
        test_data = {}
        create_access_token(data=test_data)
        assert mock_encode.call_count == 1


class TestAuthenticate:
    @patch('src.core.security.verify_password', return_value=True)
    @patch.object(DBWorker, 'get_user')
    def test_authenticate_user(self,
                               mock_get_user,
                               mock_veryfi_password):
        authenticate_user(username="test",
                          password="test")
        assert mock_get_user.call_count == 1
        assert mock_veryfi_password.call_count == 1

    @patch('src.core.security.verify_password', return_value=False)
    @patch.object(DBWorker, 'get_user')
    def test_authenticate_user_wrong_password(self,
                                              mock_get_user,
                                              mock_veryfi_password):
        result = authenticate_user(username="test",
                                   password="test")
        assert mock_get_user.call_count == 1
        assert mock_veryfi_password.call_count == 1
        assert result is False


class TestSupportFunction:
    @patch.object(CryptContext, 'verify', return_value=True)
    def test_verify_password(self, mock_verify):
        result = verify_password(plain_password='test', hashed_password='test')
        assert mock_verify.call_count == 1
        assert result is True

    @patch.object(CryptContext, 'hash', return_value=True)
    def test_get_password_hash(self, mock_hash):
        result = get_password_hash(password='test')
        assert mock_hash.call_count == 1
        assert result is True
