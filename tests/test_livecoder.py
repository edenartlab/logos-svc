from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_character_chat():
    """
    Test livecoding
    """
    request = {
        "session_id": "test",
        "message": "use a preset",
    }

    response = client.post("/livecode/code", json=request)
    print(response.json())

    assert response.status_code == 200
