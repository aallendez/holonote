from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.db.session import Base, get_db


@pytest.fixture()
def client():
    # Create a fresh in-memory SQLite DB and override get_db
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
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


def test_entries_crud_flow(client: TestClient):
    # Create
    payload = {
        "entry_date": datetime.utcnow().isoformat(),
        "title": "Entry 1",
        "content": "Content 1",
        "score": 7,
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
        "score": 9,
    }
    resp = client.put(f"/entries/{entry_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["title"] == "Updated"
    assert updated["content"] == "Updated content"
    assert updated["score"] == 9

    # Delete
    resp = client.delete(f"/entries/{entry_id}")
    assert resp.status_code == 200

    # Ensure soft-deleted doesn't show up
    resp = client.get("/entries/")
    assert resp.status_code == 200
    assert resp.json() == []


