from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_monologue():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "657926f90a0f725740a93b77", 
        "prompt": "Tell me a story about pizza"
    }

    response = client.post("/scenarios/monologue", json=request)
    print(response.json())

    assert response.status_code == 200


def test_dialogue():
    """
    Test dialogue function on static characters and prompt
    """
    request = {
        "character_ids": ["657926f90a0f725740a93b77", "657a68580a0f7257408cc55b"],
        "prompt": "Debate whether or not pizza is a vegetable"
    }

    response = client.post("/scenarios/dialogue", json=request)
    print(response.json())

    assert response.status_code == 200

