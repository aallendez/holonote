import os
from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the modules
from src.db.holos import (
    get_holo_config, 
    update_holo_config, 
    create_holo_config,
    get_holo_daily_by_date,
    get_latest_holo_daily,
    create_holo_daily,
    get_avg_score
)
from src.models.holos import HoloCreate, HoloUpdate, HoloDailyCreate, HoloTable, HoloDailiesTable
from src.db.session import Base


@pytest.fixture()
def db_session():
    """Create a database session for testing using in-memory SQLite"""
    # Shared in-memory SQLite so schema persists across connections
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create schema for tables
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up test data
        session.rollback()


@pytest.fixture()
def sample_user_id():
    return str(uuid4())


@pytest.fixture()
def test_user(db_session, sample_user_id):
    """Create a test user in the users table"""
    from src.db.users import create_user
    from src.models.users import UserCreate
    create_user(UserCreate(user_id=sample_user_id, user_name="Test User", user_email="test@example.com"), db_session)
    
    return sample_user_id


@pytest.fixture()
def sample_holo_config(sample_user_id):
    return HoloCreate(
        user_id=sample_user_id,
        questions=["How are you feeling today?", "What did you learn?", "Rate your mood"]
    )


@pytest.fixture()
def sample_holo_daily():
    return HoloDailyCreate(
        entry_date="2024-01-15",
        score=8,
        answers={"question1": "Great", "question2": "Python", "question3": 8}
    )


class TestHoloConfig:
    @pytest.fixture(autouse=True)
    def setup_test_user(self, db_session, test_user):
        """Automatically set up test user for all tests in this class"""
        pass
    
    def test_create_holo_config(self, db_session, sample_holo_config):
        """Test creating a new holo configuration"""
        result = create_holo_config(sample_holo_config.user_id, sample_holo_config, db_session)
        
        assert result is not None
        assert result.holo_id is not None
        assert result.user_id == sample_holo_config.user_id
        assert result.questions == sample_holo_config.questions
        assert result.created_at is not None

    def test_get_holo_config_existing(self, db_session, sample_user_id, sample_holo_config):
        """Test getting an existing holo configuration"""
        # Create first
        created = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        # Then get
        result = get_holo_config(sample_user_id, db_session)
        
        assert result is not None
        assert result.holo_id == created.holo_id
        assert result.user_id == sample_user_id
        assert result.questions == sample_holo_config.questions

    def test_get_holo_config_not_found(self, db_session, sample_user_id):
        """Test getting a non-existent holo configuration"""
        result = get_holo_config(sample_user_id, db_session)
        assert result is None

    def test_get_holo_config_with_nested_questions(self, db_session, sample_user_id):
        """Test getting holo config when questions are stored as nested dict"""
        # Create holo with nested questions structure
        holo_table = HoloTable(
            user_id=sample_user_id,
            questions={"questions": ["How are you?", "What did you learn?"]}
        )
        db_session.add(holo_table)
        db_session.commit()
        
        result = get_holo_config(sample_user_id, db_session)
        assert result is not None
        assert result.questions == ["How are you?", "What did you learn?"]

    def test_update_holo_config(self, db_session, sample_user_id, sample_holo_config):
        """Test updating an existing holo configuration"""
        # Create first
        created = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        # Update
        new_questions = ["New question 1", "New question 2"]
        holo_update = HoloUpdate(questions=new_questions)
        result = update_holo_config(sample_user_id, holo_update, db_session)
        
        assert result is not None
        assert result.holo_id == created.holo_id
        assert result.questions == new_questions
        assert result.updated_at is not None

    def test_update_holo_config_not_found(self, db_session, sample_user_id):
        """Test updating a non-existent holo configuration"""
        holo_update = HoloUpdate(questions=["New question"])
        result = update_holo_config(sample_user_id, holo_update, db_session)
        assert result is None


class TestHoloDaily:
    @pytest.fixture(autouse=True)
    def setup_test_user(self, db_session, test_user):
        """Automatically set up test user for all tests in this class"""
        pass
    
    def test_create_holo_daily(self, db_session, sample_user_id, sample_holo_config, sample_holo_daily):
        """Test creating a new holo daily entry"""
        # Create holo config first
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        # Create holo daily
        result = create_holo_daily(holo_config.holo_id, sample_holo_daily, db_session)
        
        assert result is not None
        assert result.holo_daily_id is not None
        assert result.holo_id == holo_config.holo_id
        assert result.entry_date == date(2024, 1, 15)
        assert result.score == 8
        assert result.answers == sample_holo_daily.answers

    def test_create_holo_daily_invalid_date_format(self, db_session, sample_user_id, sample_holo_config):
        """Test creating holo daily with invalid date format"""
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        invalid_daily = HoloDailyCreate(
            entry_date="invalid-date",
            score=5,
            answers={"test": "answer"}
        )
        
        with pytest.raises(ValueError, match="Invalid date format"):
            create_holo_daily(holo_config.holo_id, invalid_daily, db_session)

    def test_get_holo_daily_by_date(self, db_session, sample_user_id, sample_holo_config, sample_holo_daily):
        """Test getting holo daily by specific date"""
        # Create holo config and daily
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        created_daily = create_holo_daily(holo_config.holo_id, sample_holo_daily, db_session)
        
        # Get by date
        result = get_holo_daily_by_date(holo_config.holo_id, date(2024, 1, 15), db_session)
        
        assert result is not None
        assert result.holo_daily_id == created_daily.holo_daily_id
        assert result.entry_date == date(2024, 1, 15)
        assert result.score == 8

    def test_get_holo_daily_by_date_not_found(self, db_session, sample_user_id):
        """Test getting holo daily by date when it doesn't exist"""
        result = get_holo_daily_by_date(sample_user_id, date(2024, 1, 15), db_session)
        assert result is None

    def test_get_latest_holo_daily(self, db_session, sample_user_id, sample_holo_config):
        """Test getting the latest holo daily entry"""
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        # Create multiple dailies with different dates
        daily1 = HoloDailyCreate(
            entry_date="2024-01-10",
            score=5,
            answers={"test": "answer1"}
        )
        daily2 = HoloDailyCreate(
            entry_date="2024-01-15",
            score=8,
            answers={"test": "answer2"}
        )
        daily3 = HoloDailyCreate(
            entry_date="2024-01-12",
            score=7,
            answers={"test": "answer3"}
        )
        
        create_holo_daily(holo_config.holo_id, daily1, db_session)
        create_holo_daily(holo_config.holo_id, daily2, db_session)
        create_holo_daily(holo_config.holo_id, daily3, db_session)
        
        # Get latest (should be 2024-01-15)
        result = get_latest_holo_daily(holo_config.holo_id, db_session)
        
        assert result is not None
        assert result.entry_date == date(2024, 1, 15)
        assert result.score == 8

    def test_get_latest_holo_daily_not_found(self, db_session, sample_user_id):
        """Test getting latest holo daily when none exist"""
        result = get_latest_holo_daily(sample_user_id, db_session)
        assert result is None

    def test_get_avg_score(self, db_session, sample_user_id, sample_holo_config):
        """Test getting average score from holo dailies"""
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        # Create multiple dailies with different scores
        daily1 = HoloDailyCreate(
            entry_date="2024-01-10",
            score=5,
            answers={"test": "answer1"}
        )
        daily2 = HoloDailyCreate(
            entry_date="2024-01-11",
            score=7,
            answers={"test": "answer2"}
        )
        daily3 = HoloDailyCreate(
            entry_date="2024-01-12",
            score=9,
            answers={"test": "answer3"}
        )
        
        create_holo_daily(holo_config.holo_id, daily1, db_session)
        create_holo_daily(holo_config.holo_id, daily2, db_session)
        create_holo_daily(holo_config.holo_id, daily3, db_session)
        
        # Average should be (5 + 7 + 9) / 3 = 7.0
        result = get_avg_score(holo_config.holo_id, db_session)
        assert result == 7.0

    def test_get_avg_score_no_data(self, db_session, sample_user_id):
        """Test getting average score when no dailies exist"""
        result = get_avg_score(sample_user_id, db_session)
        assert result is None

    def test_get_avg_score_single_entry(self, db_session, sample_user_id, sample_holo_config, sample_holo_daily):
        """Test getting average score with single entry"""
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        create_holo_daily(holo_config.holo_id, sample_holo_daily, db_session)
        
        result = get_avg_score(holo_config.holo_id, db_session)
        assert result == 8.0  # Same as the single entry score

    def test_holo_daily_unique_constraint(self, db_session, sample_user_id, sample_holo_config, sample_holo_daily):
        """Test that holo daily enforces unique constraint on holo_id + entry_date"""
        holo_config = create_holo_config(sample_user_id, sample_holo_config, db_session)
        
        # Create first daily
        create_holo_daily(holo_config.holo_id, sample_holo_daily, db_session)
        
        # Try to create another with same date - should fail
        with pytest.raises(Exception):  # SQLAlchemy will raise an exception
            create_holo_daily(holo_config.holo_id, sample_holo_daily, db_session)