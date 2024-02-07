from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_story_characters():
    """
    Test story prompt with characters
    """

    request = {
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277", "6598e103dd06d165264f2247", "6598ee16dd06d16526503ce7"],
        "prompt": "You are members of an elite space exploration team, encountering and interpreting alien forms of art and communication."
    }

    response = client.post("/animation/story", json=request)
    print(response.json())

    assert response.status_code == 200


def test_story():
    """
    Test story prompt without characters
    """

    request = {
        "character_ids": [],
        "prompt": "A family of Dragons lives in a mystical layer underneath a volcano. The dragons are beautiful, ornately decorated, fire-breathing, creatures. They are brave and wise. The story should just be about them journeying to a bunch of beautiful far away places in nature, and then coming back to their volcano lair. Make at least 10 clips."
    }

    response = client.post("/animation/story", json=request)
    print(response.json())

    assert response.status_code == 200
