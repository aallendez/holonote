from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.entries import get_entries, create_entry, update_entry, delete_entry
from src.models.entries import EntryCreate, EntryUpdate, EntryTable
from src.db.session import Base


@pytest.fixture()
def db_session():
    # Use in-memory SQLite for fast, isolated tests
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create schema
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_and_get_entries(db_session):
    user_id = str(uuid4())

    created = create_entry(
        EntryCreate(
            user_id=user_id,
            entry_date=datetime.utcnow(),
            title="First",
            content="Hello",
        ),
        db_session,
    )

    assert created.entry_id is not None
    assert created.user_id == user_id

    results = get_entries(user_id=user_id, db=db_session)
    assert len(results) == 1
    assert results[0].title == "First"


def test_update_entry(db_session):
    user_id = str(uuid4())
    created = create_entry(
        EntryCreate(
            user_id=user_id,
            entry_date=datetime.utcnow(),
            title="Old",
            content="Old content",
        ),
        db_session,
    )

    updated = update_entry(
        created.entry_id,
        EntryUpdate(title="New", content="New content"),
        db_session,
    )

    assert updated is not None
    assert updated.title == "New"
    assert updated.content == "New content"
    assert updated.updated_at is not None


def test_delete_entry_soft_delete(db_session):
    user_id = str(uuid4())
    created = create_entry(
        EntryCreate(
            user_id=user_id,
            entry_date=datetime.utcnow(),
            title="To delete",
            content="...",
        ),
        db_session,
    )

    deleted = delete_entry(created.entry_id, db_session)
    assert deleted is not None
    assert deleted.deleted_at is not None

    # Ensure soft-deleted record is excluded from get_entries
    results = get_entries(user_id=user_id, db=db_session)
    assert results == []


def test_update_entry_not_found_returns_none(db_session):
    missing_id = str(uuid4())
    result = update_entry(
        missing_id,
        EntryUpdate(title="X", content="Y"),
        db_session,
    )
    assert result is None


def test_delete_entry_not_found_returns_none(db_session):
    missing_id = str(uuid4())
    result = delete_entry(missing_id, db_session)
    assert result is None


