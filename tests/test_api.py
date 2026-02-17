import requests
from tests.conftest import BASE_URL


def test_health_endpoint_returns_healthy():
    """Verify the API is up and running."""
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"


def test_register_user_creates_new_user(random_user):
    """Verify a new user can be created via POST /register."""
    response = requests.post(f"{BASE_URL}/api/auth/register", json=random_user)

    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == random_user.get("username")
    assert "id" in data["user"]


def test_login_returns_jwt_token(random_user):
    """Verify that logging in with valid credentials returns a token."""
    # Ensure user exists
    requests.post(f"{BASE_URL}/api/auth/register", json=random_user)

    # Attempt login
    response = requests.post(f"{BASE_URL}/api/auth/login", json=random_user)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_public_event_requires_auth_and_succeeds(auth_token):
    """Verify that an authenticated user can create an event."""
    event_data = {
        "title": "Integration Test Party",
        "description": "Testing the API live",
        "date": "2026-12-31T20:00:00",
        "location": "The Cloud",
        "is_public": True
    }

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/api/events", json=event_data, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["location"] == event_data["location"]


def test_rsvp_to_public_event_succeeds(auth_token):
    """Verify that users can RSVP to public events."""
    # 1. Create a public event (Authenticated)
    event_payload = {
        "title": "Public Gathering",
        "date": "2026-05-20T10:00:00",
        "is_public": True
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    event_resp = requests.post(f"{BASE_URL}/api/events", json=event_payload, headers=headers)
    event_id = event_resp.json()["id"]

    # 2. RSVP to it (Unauthenticated/Anonymous)
    rsvp_payload = {
        "event_id": event_id,
        "attending": True
    }

    response = requests.post(f"{BASE_URL}/api/rsvps/event/{event_id}", json=rsvp_payload)

    assert response.status_code in [200, 201]
    assert response.json()["event_id"] == event_id
