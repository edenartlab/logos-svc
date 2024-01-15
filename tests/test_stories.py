from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_cinema():
    """
    Test cinema story prompt
    """

    request = {
        "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277", "6598e103dd06d165264f2247", "6598ee16dd06d16526503ce7"],
        "prompt": "The protagonists wake up suddenly, inside of a cube-shaped chamber with 6 hatches on each wall. They have no memory of how they got there, and no idea how to escape."
    }

    response = client.post("/story/cinema", json=request)
    print(response.json())

    assert response.status_code == 200


# def test_comic():
#     """
#     Test comic book story prompt
#     """
#     request = {
#         "prompt": "Make a comic book."
#     }

#     response = client.post("/story/comic", json=request)
#     print(response.json())

#     assert response.status_code == 200
