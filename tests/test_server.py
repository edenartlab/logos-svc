from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_server():
    """
    Test if the app is running
    """
    response = client.get("/")
    assert response.json() == {"status": "running"}
