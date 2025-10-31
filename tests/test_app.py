import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Remove if already present
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Signup
    resp_signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp_unreg.status_code == 200
    assert f"removed from {activity}" in resp_unreg.json()["message"]

    # Unregister again should fail
    resp_unreg2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp_unreg2.status_code == 404
