from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_monologue_dag():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "6577e5d5c77b37642c252423", 
        "prompt": "Tell me a story about pizza"
    }

    response = client.post("/dags/monologue", json=request)
    print(response.json())

    assert response.status_code == 200


def test_dialogue_dag():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_ids": ["658fddadf0e5f5c4a0638a37", "6577e5d5c77b37642c252423"],
        "prompt": "Debate panspermia vs. abiogenesis"
    }

    response = client.post("/dags/dialogue", json=request)
    print(response.json())

    assert response.status_code == 200
