import requests
from tests.conftest import BASE_URL


def test_duplicate_username_registration_returns_400(random_user):
    """Verify that the API prevents duplicate usernames."""
    # First registration: Success
    first_resp = requests.post(f"{BASE_URL}/api/auth/register", json=random_user)
    assert first_resp.status_code == 201

    # Second registration: Failure
    second_resp = requests.post(f"{BASE_URL}/api/auth/register", json=random_user)

    assert second_resp.status_code in [400, 409]
    assert "Username already exists".lower() == second_resp.json().get("error", "").lower()


def test_create_event_without_auth_fails():
    """Verify that POST /events is protected by authentication."""
    event_payload = {
        "title": "Ghost Event",
        "date": "2026-10-10T12:00:00",
        "is_public": True
    }

    # Send request without the 'Authorization' header
    response = requests.post(f"{BASE_URL}/api/events", json=event_payload)

    assert response.status_code == 401
    assert "Missing Authorization Header".lower() == response.json().get("msg", "").lower()


def test_rsvp_to_private_event_without_auth(auth_token):
    """Verify that private events cannot be accessed/RSVPed to by anonymous users."""
    # 1. Create a PRIVATE event (requires_admin or is_public=False)
    private_event_payload = {
        "title": "Secret Meeting",
        "date": "2026-11-11T11:11:11",
        "is_public": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    event_resp = requests.post(f"{BASE_URL}/api/events", json=private_event_payload, headers=headers)
    event_id = event_resp.json()["id"]

    # 2. Try to RSVP to this private event without a token
    rsvp_payload = {
        "event_id": event_id,
        "attending": True
    }
    response = requests.post(f"{BASE_URL}/rsvps", json=rsvp_payload)

    # This should fail because the event is not public
    assert response.status_code in [401, 403, 404]
