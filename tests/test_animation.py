from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_monologue_animation():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "6596129023f1c4b471dbb94a", 
        "prompt": "Tell me a story about pizza"
    }

    response = client.post("/animation/monologue", json=request)
    print(response.json())

    assert response.status_code == 200


def test_dialogue_animation():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277"],
        "prompt": "Debate panspermia vs. abiogenesis"
    }

    response = client.post("/animation/dialogue", json=request)
    print(response.json())

    assert response.status_code == 200


def test_story_animation():
    """
    Test story generation
    """
    request = {
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277", "6598e103dd06d165264f2247", "6598ee16dd06d16526503ce7"],
        "prompt": "Debate panspermia vs. abiogenesis"
    }

    response = client.post("/animation/dialogue", json=request)
    print(response.json())

    assert response.status_code == 200


def test_comic_illustration():
    """
    Test monologue on static character and prompt
    """

    prompt = """
    - Little Martians: Verdelis
    - Setting: Simulation
    - Genre: Drama
    - Premise: Verdelis goes to outer space cosmos
    - Number of panels: 4
    """

    request = {
        "character_id": "658b44b36104b05b266ca3c6", 
        "prompt": prompt
    }

    response = client.post("/animation/comic", json=request)
    print(response.json())

    assert response.status_code == 200
