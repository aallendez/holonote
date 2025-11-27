from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

from main import app
from src.db.session import Base, get_db


@pytest.fixture()
def client():
    # Create a fresh in-memory SQLite DB and override get_db
    # Use a shared in-memory SQLite so schema persists across connections in tests
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
    # Bypass auth dependency for tests
    from src.api.routes.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"uid": "test-user"}
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_entries_crud_flow(client: TestClient):
    # Create
    payload = {
        "entry_date": datetime.utcnow().isoformat(),
        "title": "Entry 1",
        "content": "Content 1",
    }
    resp = client.post("/entries/", json=payload)
    assert resp.status_code == 200
    created = resp.json()
    entry_id = created["entry_id"]
    assert created["title"] == "Entry 1"

    # Get
    resp = client.get("/entries/")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["entry_id"] == entry_id

    # Update
    update_payload = {
        "title": "Updated",
        "content": "Updated content",
    }
    resp = client.put(f"/entries/{entry_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["title"] == "Updated"
    assert updated["content"] == "Updated content"

    # Delete
    resp = client.delete(f"/entries/{entry_id}")
    assert resp.status_code == 200

    # Ensure soft-deleted doesn't show up
    resp = client.get("/entries/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_entries_database_error(client):
    """Test get entries with database error"""
    with patch("src.api.routes.entries.get_entries") as mock_get_entries:
        mock_get_entries.side_effect = SQLAlchemyError("Database connection failed")

        response = client.get("/entries/")
        assert response.status_code == 500
        assert "Database error while fetching entries" in response.json()["detail"]


def test_get_entries_unexpected_error(client):
    """Test get entries with unexpected error"""
    with patch("src.api.routes.entries.get_entries") as mock_get_entries:
        mock_get_entries.side_effect = Exception("Unexpected error")

        response = client.get("/entries/")
        assert response.status_code == 500
        assert "Unexpected error while fetching entries" in response.json()["detail"]


def test_create_entry_validation_error(client):
    """Test create entry with validation error"""
    with patch("src.api.routes.entries.EntryCreate") as mock_entry_create:
        mock_entry_create.side_effect = ValidationError.from_exception_data(
            "ValidationError", []
        )

        payload = {
            "entry_date": "invalid-date",
            "title": "Test Entry",
            "content": "Test Content",
        }
        response = client.post("/entries/", json=payload)
        assert response.status_code == 422


def test_create_entry_integrity_error(client):
    """Test create entry with integrity error"""
    with patch("src.api.routes.entries.create_entry") as mock_create_entry:
        mock_create_entry.side_effect = IntegrityError("Integrity error", None, None)

        payload = {
            "entry_date": datetime.utcnow().isoformat(),
            "title": "Test Entry",
            "content": "Test Content",
        }
        response = client.post("/entries/", json=payload)
        assert response.status_code == 400
        assert "Data integrity error" in response.json()["detail"]


def test_create_entry_database_error(client):
    """Test create entry with database error"""
    with patch("src.api.routes.entries.create_entry") as mock_create_entry:
        mock_create_entry.side_effect = SQLAlchemyError("Database error")

        payload = {
            "entry_date": datetime.utcnow().isoformat(),
            "title": "Test Entry",
            "content": "Test Content",
        }
        response = client.post("/entries/", json=payload)
        assert response.status_code == 500
        assert "Database error while creating entry" in response.json()["detail"]


def test_create_entry_unexpected_error(client):
    """Test create entry with unexpected error"""
    with patch("src.api.routes.entries.create_entry") as mock_create_entry:
        mock_create_entry.side_effect = Exception("Unexpected error")

        payload = {
            "entry_date": datetime.utcnow().isoformat(),
            "title": "Test Entry",
            "content": "Test Content",
        }
        response = client.post("/entries/", json=payload)
        assert response.status_code == 500
        assert "Unexpected error while creating entry" in response.json()["detail"]


def test_update_entry_not_found(client):
    """Test update entry that doesn't exist"""
    update_payload = {"title": "Updated Title", "content": "Updated Content"}
    response = client.put("/entries/non-existent-id", json=update_payload)
    assert response.status_code == 404
    assert "Entry not found" in response.json()["detail"]


def test_update_entry_validation_error(client):
    """Test update entry with validation error"""
    with patch("src.api.routes.entries.update_entry") as mock_update_entry:
        mock_update_entry.side_effect = ValidationError.from_exception_data(
            "ValidationError", []
        )

        update_payload = {"title": "Updated Title", "content": "Updated Content"}
        response = client.put("/entries/test-id", json=update_payload)
        assert response.status_code == 422


def test_update_entry_database_error(client):
    """Test update entry with database error"""
    with patch("src.api.routes.entries.update_entry") as mock_update_entry:
        mock_update_entry.side_effect = SQLAlchemyError("Database error")

        update_payload = {"title": "Updated Title", "content": "Updated Content"}
        response = client.put("/entries/test-id", json=update_payload)
        assert response.status_code == 500
        assert "Database error while updating entry" in response.json()["detail"]


def test_update_entry_unexpected_error(client):
    """Test update entry with unexpected error"""
    with patch("src.api.routes.entries.update_entry") as mock_update_entry:
        mock_update_entry.side_effect = Exception("Unexpected error")

        update_payload = {"title": "Updated Title", "content": "Updated Content"}
        response = client.put("/entries/test-id", json=update_payload)
        assert response.status_code == 500
        assert "Unexpected error while updating entry" in response.json()["detail"]


def test_delete_entry_not_found(client):
    """Test delete entry that doesn't exist"""
    response = client.delete("/entries/non-existent-id")
    assert response.status_code == 404
    assert "Entry not found" in response.json()["detail"]


def test_delete_entry_database_error(client):
    """Test delete entry with database error"""
    with patch("src.api.routes.entries.delete_entry") as mock_delete_entry:
        mock_delete_entry.side_effect = SQLAlchemyError("Database error")

        response = client.delete("/entries/test-id")
        assert response.status_code == 500
        assert "Database error while deleting entry" in response.json()["detail"]


def test_delete_entry_unexpected_error(client):
    """Test delete entry with unexpected error"""
    with patch("src.api.routes.entries.delete_entry") as mock_delete_entry:
        mock_delete_entry.side_effect = Exception("Unexpected error")

        response = client.delete("/entries/test-id")
        assert response.status_code == 500
        assert "Unexpected error while deleting entry" in response.json()["detail"]
