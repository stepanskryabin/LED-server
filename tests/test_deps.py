from unittest.mock import patch

import pytest
from jose import jwt

from src.core.deps import CredentialsError
from src.core.deps import get_auth_token
from src.db.worker import DBWorker
from src.core.deps import check_auth_token
from src.schemas.schemas import UserDBResult


class TestDeps:
    class TestGetAuthToken:
        def test_get_auth_token(self, fx_user):
            result = get_auth_token(user=fx_user)
            assert isinstance(result, str)

    class TestCheckAuthToken:
        @patch.object(DBWorker, 'get_user')
        @patch.object(jwt, 'decode')
        def test_unit(self, mock_decode, mock_db):
            result = check_auth_token(token="test")
            assert mock_decode.call_count == 1
            assert mock_db.call_count == 1
            assert result is None

        def test_error_jwt_decode(self):
            with pytest.raises(CredentialsError):
                check_auth_token(token="test")

        @patch.object(jwt, 'decode')
        @patch.object(DBWorker,
                      'get_user',
                      return_value=UserDBResult())
        def test_error_db_user_is_none(self, mock_db, mock_decode):
            _ = mock_db, mock_decode
            with pytest.raises(CredentialsError):
                check_auth_token(token="test")

        @patch.object(jwt, 'decode')
        @patch.object(DBWorker,
                      'get_user',
                      return_value=UserDBResult(is_activated=False))
        def test_error_db_user_is_not_activated(self, mock_db, mock_decode):
            _ = mock_db, mock_decode
            with pytest.raises(CredentialsError):
                check_auth_token(token="test")
