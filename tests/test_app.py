from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Debate Club" in data
    assert isinstance(data["Debate Club"]["participants"], list)
    assert "alex@mergington.edu" in data["Debate Club"]["participants"]


def test_signup_and_remove_participant():
    activity = "Debate Club"
    email = "testuser@example.com"

    # Ensure not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email not in data[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    # Verify participant added
    resp = client.get("/activities")
    data = resp.json()
    assert email in data[activity]["participants"]

    # Remove participant
    resp = client.delete(f"/activities/{activity}/participant?email={email}")
    assert resp.status_code == 200
    assert f"Removed {email}" in resp.json().get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]
