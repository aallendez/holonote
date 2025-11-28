import pytest
from fastapi.testclient import TestClient

# Import the modules
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.db.session import Base, get_db
from src.db.users import create_user
from src.models.users import UserCreate


@pytest.fixture()
def client():
    """Create a test client with in-memory SQLite database"""
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


@pytest.fixture()
def test_user(client):
    """Create a test user in the database"""
    from src.db.session import get_db
    from src.db.users import user_exists

    # Use the overridden get_db from the app to ensure SQLite is used
    override = app.dependency_overrides[get_db]
    db = next(override())
    try:
        # Only create user if it doesn't exist
        if not user_exists("test-user", db):
            user_create = UserCreate(
                user_id="test-user",
                user_name="Test User",
                user_email="test@example.com",
            )
            create_user(user_create, db)
        yield
    finally:
        db.close()


@pytest.fixture()
def clean_holo_config(client):
    """Clean up any existing holo config for test user"""
    from sqlalchemy import delete
    from src.db.session import get_db
    from src.models.holos import HoloTable

    override = app.dependency_overrides[get_db]
    db = next(override())
    try:
        # Delete any existing holo config for test-user
        db.execute(delete(HoloTable).where(HoloTable.user_id == "test-user"))
        db.commit()
        yield
    finally:
        db.close()


@pytest.fixture()
def sample_holo_config():
    return {
        "user_id": "test-user",
        "questions": [
            "How are you feeling today?",
            "What did you learn?",
            "Rate your mood",
        ],
    }


@pytest.fixture()
def sample_holo_daily():
    return {
        "entry_date": "2024-01-15",
        "score": 8,
        "answers": {"question1": "Great", "question2": "Python", "question3": 8},
    }


class TestHoloConfigAPI:
    @pytest.fixture(autouse=True)
    def setup_test_data(self, client, test_user, clean_holo_config):
        """Automatically set up test data for all tests in this class"""
        pass

    def test_create_holo_config(self, client, sample_holo_config):
        """Test creating a new holo configuration via API"""
        response = client.post("/holos/holo", json=sample_holo_config)
        assert response.status_code == 200

        data = response.json()
        assert data["holo_id"] is not None
        assert data["user_id"] == "test-user"
        assert data["questions"] == sample_holo_config["questions"]

    def test_get_holo_config_not_found(self, client):
        """Test getting holo config when it doesn't exist"""
        response = client.get("/holos/holo")
        assert response.status_code == 404
        assert "Holo configuration not found" in response.json()["detail"]

    def test_get_holo_config_existing(self, client, sample_holo_config):
        """Test getting an existing holo configuration"""
        # Create first
        create_response = client.post("/holos/holo", json=sample_holo_config)
        assert create_response.status_code == 200

        # Then get
        get_response = client.get("/holos/holo")
        assert get_response.status_code == 200

        data = get_response.json()
        assert data["user_id"] == "test-user"
        assert data["questions"] == sample_holo_config["questions"]

    def test_update_holo_config_not_found(self, client):
        """Test updating holo config when it doesn't exist"""
        update_data = {"questions": ["New question"]}
        response = client.put("/holos/holo", json=update_data)
        assert response.status_code == 404
        assert "Holo configuration not found" in response.json()["detail"]

    def test_update_holo_config_existing(self, client, sample_holo_config):
        """Test updating an existing holo configuration"""
        # Create first
        create_response = client.post("/holos/holo", json=sample_holo_config)
        assert create_response.status_code == 200

        # Update
        new_questions = ["Updated question 1", "Updated question 2"]
        update_data = {"questions": new_questions}
        update_response = client.put("/holos/holo", json=update_data)
        assert update_response.status_code == 200

        data = update_response.json()
        assert data["questions"] == new_questions

    def test_create_holo_config_validation_error(self, client):
        """Test creating holo config with invalid data"""
        invalid_data = {"questions": "not a list"}  # Should be list
        response = client.post("/holos/holo", json=invalid_data)
        assert response.status_code == 422

    def test_update_holo_config_validation_error(self, client, sample_holo_config):
        """Test updating holo config with invalid data"""
        # Create first
        client.post("/holos/holo", json=sample_holo_config)

        # Try to update with invalid data
        invalid_data = {"questions": "not a list"}
        response = client.put("/holos/holo", json=invalid_data)
        assert response.status_code == 422


class TestHoloDailyAPI:
    @pytest.fixture(autouse=True)
    def setup_test_data(self, client, test_user, clean_holo_config):
        """Automatically set up test data for all tests in this class"""
        pass

    def test_get_holo_daily_no_config(self, client):
        """Test getting holo daily when no holo config exists"""
        response = client.get("/holos/daily?entry_date=2024-01-15")
        assert response.status_code == 404
        assert "No holo config found" in response.json()["detail"]

    def test_get_holo_daily_with_config_no_daily(self, client, sample_holo_config):
        """Test getting holo daily when config exists but no daily for date"""
        # Create holo config
        client.post("/holos/holo", json=sample_holo_config)

        # Try to get daily for date that doesn't exist
        response = client.get("/holos/daily?entry_date=2024-01-15")
        assert response.status_code == 404
        assert "Holo daily not found" in response.json()["detail"]

    def test_create_holo_daily_no_config(self, client, sample_holo_daily):
        """Test creating holo daily when no holo config exists"""
        response = client.post("/holos/daily", json=sample_holo_daily)
        assert response.status_code == 404
        assert "No holo config found" in response.json()["detail"]

    def test_create_holo_daily_success(
        self, client, sample_holo_config, sample_holo_daily
    ):
        """Test creating holo daily successfully"""
        # Create holo config first
        config_response = client.post("/holos/holo", json=sample_holo_config)
        assert config_response.status_code == 200

        # Create holo daily
        daily_response = client.post("/holos/daily", json=sample_holo_daily)
        assert daily_response.status_code == 200

        data = daily_response.json()
        assert data["holo_daily_id"] is not None
        assert data["entry_date"] == "2024-01-15"
        assert data["score"] == 8
        assert data["answers"] == sample_holo_daily["answers"]

    def test_get_holo_daily_by_date_success(
        self, client, sample_holo_config, sample_holo_daily
    ):
        """Test getting holo daily by specific date"""
        # Create holo config and daily
        config_response = client.post("/holos/holo", json=sample_holo_config)
        daily_response = client.post("/holos/daily", json=sample_holo_daily)

        # Get by date
        get_response = client.get("/holos/daily?entry_date=2024-01-15")
        assert get_response.status_code == 200

        data = get_response.json()
        assert data["entry_date"] == "2024-01-15"
        assert data["score"] == 8

    def test_get_latest_holo_daily_no_config(self, client):
        """Test getting latest holo daily when no config exists"""
        response = client.get("/holos/daily/latest")
        assert response.status_code == 404
        assert "No holo config found" in response.json()["detail"]

    def test_get_latest_holo_daily_no_dailies(self, client, sample_holo_config):
        """Test getting latest holo daily when no dailies exist"""
        # Create holo config
        client.post("/holos/holo", json=sample_holo_config)

        # Try to get latest daily
        response = client.get("/holos/daily/latest")
        assert response.status_code == 404
        assert "No holo daily found" in response.json()["detail"]

    def test_get_latest_holo_daily_success(self, client, sample_holo_config):
        """Test getting latest holo daily successfully"""
        # Create holo config
        config_response = client.post("/holos/holo", json=sample_holo_config)

        # Create multiple dailies
        daily1 = {
            "entry_date": "2024-01-10",
            "score": 5,
            "answers": {"test": "answer1"},
        }
        daily2 = {
            "entry_date": "2024-01-15",
            "score": 8,
            "answers": {"test": "answer2"},
        }

        client.post("/holos/daily", json=daily1)
        client.post("/holos/daily", json=daily2)

        # Get latest (should be 2024-01-15)
        response = client.get("/holos/daily/latest")
        assert response.status_code == 200

        data = response.json()
        assert data["entry_date"] == "2024-01-15"
        assert data["score"] == 8

    def test_create_holo_daily_validation_error(self, client, sample_holo_config):
        """Test creating holo daily with invalid data"""
        # Create holo config
        client.post("/holos/holo", json=sample_holo_config)

        # Try to create daily with invalid data
        invalid_daily = {
            "entry_date": "invalid-date",
            "score": "not a number",
            "answers": "not a dict",
        }
        response = client.post("/holos/daily", json=invalid_daily)
        assert response.status_code == 422

    def test_create_holo_daily_invalid_date_format(self, client, sample_holo_config):
        """Test creating holo daily with invalid date format"""
        # Create holo config
        client.post("/holos/holo", json=sample_holo_config)

        # Try to create daily with invalid date format
        invalid_daily = {
            "entry_date": "invalid-date",
            "score": 5,
            "answers": {"test": "answer"},
        }
        response = client.post("/holos/daily", json=invalid_daily)
        assert response.status_code == 422


class TestHoloAvgScoreAPI:
    @pytest.fixture(autouse=True)
    def setup_test_data(self, client, test_user, clean_holo_config):
        """Automatically set up test data for all tests in this class"""
        pass

    def test_get_avg_score_no_config(self, client):
        """Test getting average score when no holo config exists"""
        response = client.get("/holos/avg-score")
        assert response.status_code == 404
        assert "No holo config found" in response.json()["detail"]

    def test_get_avg_score_no_dailies(self, client, sample_holo_config):
        """Test getting average score when no dailies exist"""
        # Create holo config
        client.post("/holos/holo", json=sample_holo_config)

        # Get average score
        response = client.get("/holos/avg-score")
        assert response.status_code == 200

        data = response.json()
        assert data["avg_score"] is None

    def test_get_avg_score_success(self, client, sample_holo_config):
        """Test getting average score successfully"""
        # Create holo config
        config_response = client.post("/holos/holo", json=sample_holo_config)
        assert config_response.status_code == 200

        # Create multiple dailies with different scores
        dailies = [
            {"entry_date": "2024-01-10", "score": 5, "answers": {"test": "answer1"}},
            {"entry_date": "2024-01-11", "score": 7, "answers": {"test": "answer2"}},
            {"entry_date": "2024-01-12", "score": 9, "answers": {"test": "answer3"}},
        ]

        for daily in dailies:
            client.post("/holos/daily", json=daily)

        # Get average score (should be 7.0)
        response = client.get("/holos/avg-score")
        assert response.status_code == 200

        data = response.json()
        assert data["avg_score"] == 7.0

    def test_get_avg_score_single_entry(
        self, client, sample_holo_config, sample_holo_daily
    ):
        """Test getting average score with single entry"""
        # Create holo config
        client.post("/holos/holo", json=sample_holo_config)

        # Create single daily
        client.post("/holos/daily", json=sample_holo_daily)

        # Get average score
        response = client.get("/holos/avg-score")
        assert response.status_code == 200

        data = response.json()
        assert data["avg_score"] == 8.0  # Same as single entry score


class TestHoloCRUDFlow:
    @pytest.fixture(autouse=True)
    def setup_test_data(self, client, test_user, clean_holo_config):
        """Automatically set up test data for all tests in this class"""
        pass

    def test_complete_holo_workflow(self, client, sample_holo_config):
        """Test complete CRUD workflow for holos"""
        # 1. Create holo config
        config_response = client.post("/holos/holo", json=sample_holo_config)
        assert config_response.status_code == 200
        config_data = config_response.json()

        # 2. Get holo config
        get_response = client.get("/holos/holo")
        assert get_response.status_code == 200
        assert get_response.json()["questions"] == sample_holo_config["questions"]

        # 3. Update holo config
        new_questions = ["Updated question 1", "Updated question 2"]
        update_response = client.put("/holos/holo", json={"questions": new_questions})
        assert update_response.status_code == 200
        assert update_response.json()["questions"] == new_questions

        # 4. Create multiple holo dailies
        dailies = [
            {"entry_date": "2024-01-10", "score": 5, "answers": {"q1": "answer1"}},
            {"entry_date": "2024-01-11", "score": 8, "answers": {"q1": "answer2"}},
            {"entry_date": "2024-01-12", "score": 7, "answers": {"q1": "answer3"}},
        ]

        for daily in dailies:
            daily_response = client.post("/holos/daily", json=daily)
            assert daily_response.status_code == 200

        # 5. Get daily by date
        specific_response = client.get("/holos/daily?entry_date=2024-01-11")
        assert specific_response.status_code == 200
        assert specific_response.json()["score"] == 8

        # 6. Get latest daily
        latest_response = client.get("/holos/daily/latest")
        assert latest_response.status_code == 200
        assert latest_response.json()["entry_date"] == "2024-01-12"

        # 7. Get average score
        avg_response = client.get("/holos/avg-score")
        assert avg_response.status_code == 200
        assert (
            avg_response.json()["avg_score"] == 6.67
        )  # (5+8+7)/3 rounded to 2 decimals
