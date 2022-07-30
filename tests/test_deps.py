from unittest.mock import patch

from jose import jwt

from src.core.deps import get_auth_token
from src.db.worker import DBWorker
from src.core.deps import check_auth_token


class TestAuthToken:
    @patch.object(DBWorker, 'get_user')
    @patch.object(jwt, 'decode')
    @patch('fastapi.Depends')
    def test_get_auth_token(self, _, mock_decode, mock_db):
        result = get_auth_token(token="test")
        assert mock_decode.call_count == 1
        assert mock_db.call_count == 1
        assert result is None

    @patch.object(DBWorker, 'get_user')
    @patch.object(jwt, 'decode')
    @patch('fastapi.Header')
    def test_check_auth_token(self, _, mock_decode, mock_db):
        result = check_auth_token(token="test")
        assert mock_decode.call_count == 1
        assert mock_db.call_count == 1
        assert result is None
