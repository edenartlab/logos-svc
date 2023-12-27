from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """
    Test if the app is running
    """
    response = client.get("/")
    assert response.json() == {"status": "running"}


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


def test_chat():
    """
    Test chat function on static character and prompt
    """
    request = {
        "character_id": "657926f90a0f725740a93b77",
        "session_id": "default",
        "prompt": "I want to make a video which morphs between these two picture ideas I have. I want the video to start like a lush tropical forest with birds and nature and fireflies and stuff. And then it should evolve into a sketchy mountain scene with two moons."
    }

    response = client.post("/scenarios/chat", json=request)
    print(response.json())

    assert response.status_code == 200


def test_story():
    """
    Test story function prompt
    """
    request = {
        "prompt": "Tell a story."
    }

    response = client.post("/story", json=request)
    print(response.json())

    assert response.status_code == 200


test_read_main()
test_monologue()
test_dialogue()
test_chat()
test_story()



# from app.scenarios import Agent

# agent = Agent("657926f90a0f725740a93b77")

# print(agent)
# print(agent.character_id)