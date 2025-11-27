import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from src.db.session import Base, get_db


@pytest.fixture()
def client():
    # Create a fresh in-memory SQLite DB and override get_db
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class TestAuthAPI:
    def test_protected_route_success(self, client):
        """Test accessing protected route with valid token"""
        with patch("src.api.routes.auth.verify_token_and_ensure_user") as mock_verify:
            mock_verify.return_value = {"uid": "test-user", "email": "test@example.com"}

            response = client.get(
                "/auth/protected", headers={"Authorization": "Bearer valid-token"}
            )
            assert response.status_code == 200
            assert (
                "Hello test-user, you are authenticated!" in response.json()["message"]
            )

    def test_protected_route_invalid_header(self, client):
        """Test accessing protected route with invalid authorization header"""
        response = client.get(
            "/auth/protected", headers={"Authorization": "Invalid token"}
        )
        assert response.status_code == 401
        assert "Invalid authorization header" in response.json()["detail"]

    def test_protected_route_no_header(self, client):
        """Test accessing protected route without authorization header"""
        response = client.get("/auth/protected")
        assert response.status_code == 422  # Missing required header

    def test_protected_route_invalid_token(self, client):
        """Test accessing protected route with invalid token"""
        with patch("src.api.routes.auth.verify_token_and_ensure_user") as mock_verify:
            mock_verify.return_value = None

            response = client.get(
                "/auth/protected", headers={"Authorization": "Bearer invalid-token"}
            )
            assert response.status_code == 401
            assert "Invalid or expired token" in response.json()["detail"]

    def test_protected_route_exception(self, client):
        """Test accessing protected route when token verification raises exception"""
        with patch("src.api.routes.auth.verify_token_and_ensure_user") as mock_verify:
            mock_verify.side_effect = Exception("Token verification failed")

            response = client.get(
                "/auth/protected", headers={"Authorization": "Bearer token"}
            )
            assert response.status_code == 401
            assert "Invalid or expired token" in response.json()["detail"]

    def test_get_user_info_success(self, client):
        """Test getting user info with valid token"""
        with patch("src.api.routes.auth.verify_token_and_ensure_user") as mock_verify:
            mock_verify.return_value = {
                "uid": "test-user",
                "email": "test@example.com",
                "user_data": {"user_id": "test-user", "user_name": "Test User"},
            }

            response = client.get(
                "/auth/user-info", headers={"Authorization": "Bearer valid-token"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["firebase_uid"] == "test-user"
            assert data["user_data"]["user_id"] == "test-user"

    def test_get_user_info_no_user_data(self, client):
        """Test getting user info when no user_data is present"""
        with patch("src.api.routes.auth.verify_token_and_ensure_user") as mock_verify:
            mock_verify.return_value = {"uid": "test-user", "email": "test@example.com"}

            response = client.get(
                "/auth/user-info", headers={"Authorization": "Bearer valid-token"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["firebase_uid"] == "test-user"
            assert data["user_data"] == {}
