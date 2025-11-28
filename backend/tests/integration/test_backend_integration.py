import sys
from datetime import date, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app
from src.api.routes.auth import get_current_user
from src.db.session import Base, get_db
from src.models.users import UserTable

TEST_USER = {
    "uid": "test-user",
    "user_name": "Test User",
    "user_email": "test@example.com",
}


@pytest.fixture()
def client():
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
    app.dependency_overrides[get_current_user] = lambda: {
        "uid": TEST_USER["uid"],
        "email": TEST_USER["user_email"],
        "name": TEST_USER["user_name"],
    }

    session = TestingSessionLocal()
    try:
        session.add(
            UserTable(
                user_id=TEST_USER["uid"],
                user_name=TEST_USER["user_name"],
                user_email=TEST_USER["user_email"],
            )
        )
        session.commit()
    finally:
        session.close()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


pytestmark = pytest.mark.integration


def test_entries_crud_flow(client: TestClient):
    entry_date = datetime.utcnow().isoformat()
    payload = {
        "entry_date": entry_date,
        "title": "Entry 1",
        "content": "Content 1",
    }
    create_resp = client.post("/entries/", json=payload)
    assert create_resp.status_code == 200
    created_entry = create_resp.json()

    list_resp = client.get("/entries/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    update_payload = {"title": "Updated title", "content": "Updated content"}
    update_resp = client.put(
        f"/entries/{created_entry['entry_id']}", json=update_payload
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated title"

    delete_resp = client.delete(f"/entries/{created_entry['entry_id']}")
    assert delete_resp.status_code == 200

    final_list = client.get("/entries/")
    assert final_list.status_code == 200
    assert final_list.json() == []


def test_holo_config_and_daily_flow(client: TestClient):
    create_config_resp = client.post(
        "/holos/holo",
        json={"user_id": "ignored", "questions": ["Q1", "Q2"]},
    )
    assert create_config_resp.status_code == 200
    holo_id = create_config_resp.json()["holo_id"]
    assert holo_id

    update_resp = client.put("/holos/holo", json={"questions": ["Q3"]})
    assert update_resp.status_code == 200
    assert update_resp.json()["questions"] == ["Q3"]

    first_entry_date = date(2024, 1, 1).isoformat()
    second_entry_date = date(2024, 1, 2).isoformat()

    daily_payload = {
        "entry_date": first_entry_date,
        "score": 4,
        "answers": {"Q3": True},
    }
    daily_resp = client.post("/holos/daily", json=daily_payload)
    assert daily_resp.status_code == 200
    assert daily_resp.json()["score"] == 4

    second_resp = client.post(
        "/holos/daily",
        json={
            "entry_date": second_entry_date,
            "score": 6,
            "answers": {"Q3": False},
        },
    )
    assert second_resp.status_code == 200

    get_daily = client.get(f"/holos/daily?entry_date={first_entry_date}")
    assert get_daily.status_code == 200
    assert get_daily.json()["entry_date"] == first_entry_date

    latest_resp = client.get("/holos/daily/latest")
    assert latest_resp.status_code == 200
    assert latest_resp.json()["entry_date"] == second_entry_date
    assert latest_resp.json()["holo_id"] == holo_id

    avg_resp = client.get("/holos/avg-score")
    assert avg_resp.status_code == 200
    assert avg_resp.json()["avg_score"] == 5.0
