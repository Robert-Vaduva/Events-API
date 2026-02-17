import pytest
import uuid
import requests

BASE_URL = "http://localhost:5000"


@pytest.fixture
def random_user():
    """Generates a unique username and password for testing."""
    unique_id = uuid.uuid4().hex[:6]
    return {
        "username": f"user_{unique_id}",
        "password": "testpassword123"
    }


@pytest.fixture
def auth_token(random_user):
    """Registers a user and returns a valid JWT access token."""
    requests.post(f"{BASE_URL}/api/auth/register", json=random_user)
    response = requests.post(f"{BASE_URL}/api/auth/login", json=random_user)
    return response.json().get("access_token")
