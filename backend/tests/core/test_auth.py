import pytest
from unittest.mock import patch, MagicMock
from src.core.auth import verify_token, verify_token_and_ensure_user

class TestAuthCore:
    def test_verify_token_success(self):
        """Test successful token verification"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify:
            mock_verify.return_value = {"uid": "test-user", "email": "test@example.com"}
            
            result = verify_token("valid-token")
            assert result == {"uid": "test-user", "email": "test@example.com"}

    def test_verify_token_failure(self):
        """Test token verification failure"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")
            
            result = verify_token("invalid-token")
            assert result is None

    def test_verify_token_and_ensure_user_success(self):
        """Test successful token verification with user creation"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify, \
             patch('src.core.auth.SessionLocal') as mock_session_local, \
             patch('src.core.auth.ensure_user_exists') as mock_ensure_user:
            
            mock_verify.return_value = {"uid": "test-user", "email": "test@example.com"}
            mock_db = MagicMock()
            mock_session_local.return_value = mock_db
            mock_ensure_user.return_value = {"user_id": "test-user", "user_name": "Test User"}
            
            result = verify_token_and_ensure_user("valid-token")
            
            assert result is not None
            assert result["uid"] == "test-user"
            assert result["user_data"]["user_id"] == "test-user"
            mock_db.close.assert_called_once()

    def test_verify_token_and_ensure_user_invalid_token(self):
        """Test token verification with invalid token"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")
            
            result = verify_token_and_ensure_user("invalid-token")
            assert result is None

    def test_verify_token_and_ensure_user_no_token(self):
        """Test token verification with None token"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify:
            mock_verify.return_value = None
            
            result = verify_token_and_ensure_user("token")
            assert result is None

    def test_verify_token_and_ensure_user_no_user_data(self):
        """Test token verification when user creation fails"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify, \
             patch('src.core.auth.SessionLocal') as mock_session_local, \
             patch('src.core.auth.ensure_user_exists') as mock_ensure_user:
            
            mock_verify.return_value = {"uid": "test-user", "email": "test@example.com"}
            mock_db = MagicMock()
            mock_session_local.return_value = mock_db
            mock_ensure_user.return_value = None
            
            result = verify_token_and_ensure_user("valid-token")
            
            assert result is None
            mock_db.close.assert_called_once()

    def test_verify_token_and_ensure_user_exception(self):
        """Test token verification when exception occurs"""
        with patch('src.core.auth.auth.verify_id_token') as mock_verify:
            mock_verify.side_effect = Exception("Firebase error")
            
            result = verify_token_and_ensure_user("token")
            assert result is None
