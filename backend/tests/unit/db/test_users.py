import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.session import Base
from src.db.users import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
    user_exists,
)
from src.models.users import UserCreate, UserUpdate


@pytest.fixture()
def db_session():
    """Create a database session for testing"""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def sample_user_data():
    return {
        "user_id": "test-user-123",
        "user_name": "Test User",
        "user_email": "test@example.com",
    }


class TestUsersDB:
    def test_get_user_by_id_existing(self, db_session, sample_user_data):
        """Test getting an existing user by ID"""
        # Create a user first
        user_create = UserCreate(**sample_user_data)
        created_user = create_user(user_create, db_session)

        # Get user by ID
        result = get_user_by_id(sample_user_data["user_id"], db_session)

        assert result is not None
        assert result.user_id == sample_user_data["user_id"]
        assert result.user_name == sample_user_data["user_name"]
        assert result.user_email == sample_user_data["user_email"]

    def test_get_user_by_id_not_found(self, db_session):
        """Test getting a user by ID when user doesn't exist"""
        result = get_user_by_id("non-existent-user", db_session)
        assert result is None

    def test_get_user_by_email_existing(self, db_session, sample_user_data):
        """Test getting an existing user by email"""
        # Create a user first
        user_create = UserCreate(**sample_user_data)
        create_user(user_create, db_session)

        # Get user by email
        result = get_user_by_email(sample_user_data["user_email"], db_session)

        assert result is not None
        assert result.user_id == sample_user_data["user_id"]
        assert result.user_email == sample_user_data["user_email"]

    def test_get_user_by_email_not_found(self, db_session):
        """Test getting a user by email when user doesn't exist"""
        result = get_user_by_email("nonexistent@example.com", db_session)
        assert result is None

    def test_create_user_success(self, db_session, sample_user_data):
        """Test creating a new user successfully"""
        user_create = UserCreate(**sample_user_data)
        result = create_user(user_create, db_session)

        assert result is not None
        assert result.user_id == sample_user_data["user_id"]
        assert result.user_name == sample_user_data["user_name"]
        assert result.user_email == sample_user_data["user_email"]
        assert result.created_at is not None

    def test_update_user_success(self, db_session, sample_user_data):
        """Test updating an existing user successfully"""
        # Create a user first
        user_create = UserCreate(**sample_user_data)
        create_user(user_create, db_session)

        # Update user
        update_data = UserUpdate(
            user_name="Updated Name", user_email="updated@example.com"
        )
        result = update_user(sample_user_data["user_id"], update_data, db_session)

        assert result is not None
        assert result.user_name == "Updated Name"
        assert result.user_email == "updated@example.com"

    def test_update_user_partial(self, db_session, sample_user_data):
        """Test updating user with partial data"""
        # Create a user first
        user_create = UserCreate(**sample_user_data)
        create_user(user_create, db_session)

        # Update only name
        update_data = UserUpdate(user_name="Updated Name")
        result = update_user(sample_user_data["user_id"], update_data, db_session)

        assert result is not None
        assert result.user_name == "Updated Name"
        assert (
            result.user_email == sample_user_data["user_email"]
        )  # Should remain unchanged

    def test_update_user_not_found(self, db_session):
        """Test updating a user that doesn't exist"""
        update_data = UserUpdate(user_name="Updated Name")
        result = update_user("non-existent-user", update_data, db_session)
        assert result is None

    def test_delete_user_success(self, db_session, sample_user_data):
        """Test soft deleting a user successfully"""
        # Create a user first
        user_create = UserCreate(**sample_user_data)
        create_user(user_create, db_session)

        # Delete user
        result = delete_user(sample_user_data["user_id"], db_session)

        assert result is not None
        assert result.deleted_at is not None
        assert result.user_id == sample_user_data["user_id"]

    def test_delete_user_not_found(self, db_session):
        """Test deleting a user that doesn't exist"""
        result = delete_user("non-existent-user", db_session)
        assert result is None

    def test_user_exists_true(self, db_session, sample_user_data):
        """Test user_exists returns True for existing user"""
        # Create a user first
        user_create = UserCreate(**sample_user_data)
        create_user(user_create, db_session)

        # Check if user exists
        result = user_exists(sample_user_data["user_id"], db_session)
        assert result is True

    def test_user_exists_false(self, db_session):
        """Test user_exists returns False for non-existing user"""
        result = user_exists("non-existent-user", db_session)
        assert result is False
