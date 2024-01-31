from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_monologue():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "6596129023f1c4b471dbb94a", 
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
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277"],
        "prompt": "Debate whether or not pizza is a vegetable"
    }

    response = client.post("/scenarios/dialogue", json=request)
    print(response.json())

    assert response.status_code == 200



def test_story():
    """
    Test dialogue function on static characters and prompt
    """
    request = {
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277"],
        "prompt": "Debate whether or not pizza is a vegetable"
    }

    response = client.post("/scenarios/story", json=request)
    print(response.json())

    assert response.status_code == 200



def test_comic():
    """
    Test dialogue function on static characters and prompt
    """
    request = {
        "character_id": "658b44b36104b05b266ca3c6", #"658b481a6104b05b266eaed6", #"658b44b36104b05b266ca3c6", # "658b481a6104b05b266eaed6"], 
        "prompt": "Debate whether or not pizza is a vegetable"
    }

    response = client.post("/scenarios/comic", json=request)
    print(response.json())

    assert response.status_code == 200
