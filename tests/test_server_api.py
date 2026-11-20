from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify health endpoint responds with standard status structure."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["service"] == "Spring Money AI Agent"
    assert "timestamp" in data


def test_diagnostics_endpoint():
    """Verify diagnostics reports configuration parameters."""
    response = client.get("/api/v1/diagnostics")
    assert response.status_code == 200
    data = response.json()
    assert "config" in data
    assert "valid" in data
