from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from main import Base, app, get_db  # noqa: E402

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_read_workouts():
    response = client.get("/workouts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_workout():
    dummy_workout = {
        "exercise_name": "Automated Test Squat",
        "sets": 3,
        "reps": 10,
        "weight": 135.0
    }
    response = client.post("/workouts/", json=dummy_workout)
    assert response.status_code == 200
    assert response.json()["exercise_name"] == "Automated Test Squat"
    assert "id" in response.json()


def test_create_workout_missing_data():
    bad_workout = {
        "exercise_name": "Automated Test Bench",
        "sets": 3,
        "reps": 10,
    }
    response = client.post("/workouts/", json=bad_workout)
    assert response.status_code == 422
    assert "weight" in response.json()["detail"][0]["loc"]
