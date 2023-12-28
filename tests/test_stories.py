from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_cinema():
    """
    Test cinema story prompt
    """
    request = {
        "prompt": "Tell a story."
    }

    response = client.post("/story/cinema", json=request)
    print(response.json())

    assert response.status_code == 200


def test_comic():
    """
    Test comic book story prompt
    """
    request = {
        "prompt": "Make a comic book."
    }

    response = client.post("/story/comic", json=request)
    print(response.json())

    assert response.status_code == 200
