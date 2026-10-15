import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

ORIGINAL = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore the in-memory data before each test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL))
    yield


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_all(client):
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_success(client):
    # Arrange
    email = "newstudent@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_rejected(client):
    # Arrange
    email = "michael@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_signup_unknown_activity(client):
    # Act
    response = client.post("/activities/Nope/signup", params={"email": "a@b.edu"})
    # Assert
    assert response.status_code == 404
