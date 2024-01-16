from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_story():
    """
    Test story prompt
    """

    request = {
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277", "6598e103dd06d165264f2247", "6598ee16dd06d16526503ce7"],
        "prompt": "You are members of an elite space exploration team, encountering and interpreting alien forms of art and communication."
    }

    response = client.post("/animation/story", json=request)
    print(response.json())

    assert response.status_code == 200
