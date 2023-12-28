from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_chat():
    """
    Test chat function on static character and prompt
    """
    request = {
        "character_id": "657926f90a0f725740a93b77",
        "session_id": "default",
        "prompt": "I want to make a video which morphs between these two picture ideas I have. I want the video to start like a lush tropical forest with birds and nature and fireflies and stuff. And then it should evolve into a sketchy mountain scene with two moons."
    }

    response = client.post("/chat/speak", json=request)
    print(response.json())

    assert response.status_code == 200


def test_testchat():
    """
    Test frontend testing chat function on in-progress character and prompt
    """
    request = {
        "name": "Abraham",
        "identity": "Abraham is an autonomous artificial artist",
        "prompt": "Who are you?",
        "knowledge_summary": None,
        "knowledge": None
    }

    response = client.post("/chat/test", json=request)
    print(response.json())

    assert response.status_code == 200
