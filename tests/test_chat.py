from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_edencharacter_chat():
    """
    Test chat function on static character and prompt
    """
    request = {
        "character_id": "6596129023f1c4b471dbb94a",
        "session_id": "default",
        "message": "I want to make a video which morphs between these two picture ideas I have. I want the video to start like a lush tropical forest with birds and nature and fireflies and stuff. And then it should evolve into a sketchy mountain scene with two moons.",
        "attachments": [],
    }

    response = client.post("/chat/speak", json=request)
    print(response.json())

    assert response.status_code == 200


def test_character_chat():
    """
    Test frontend testing chat function on in-progress character and prompt
    """
    request = {
        "name": "Abraham",
        "identity": "Abraham is an autonomous artificial artist",
        "message": "Who are you?",
        "attachments": None,
        "knowledge_summary": None,
        "knowledge": None,
    }

    response = client.post("/chat/test", json=request)
    print(response.json())

    assert response.status_code == 200
