from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_monologue():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "6577e5d5c77b37642c252423", 
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
        "character_ids": ["6577e5d5c77b37642c252423", "658fddadf0e5f5c4a0638a37"],
        "prompt": "Debate whether or not pizza is a vegetable"
    }

    response = client.post("/scenarios/dialogue", json=request)
    print(response.json())

    assert response.status_code == 200
