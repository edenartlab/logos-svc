from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_monologue_dag():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "657926f90a0f725740a93b77", 
        "prompt": "Tell me a story about pizza"
    }

    response = client.post("/dags/monologue", json=request)
    print(response.json())

    assert response.status_code == 200
