from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


# def test_monologue():
#     """
#     Test making a generator request for a monologue
#     """
    
#     request = {
#         "generatorName": "monologue",
#         "config": {
#             "characterId": "6596129023f1c4b471dbb94a",
#             "prompt": "Who are you?",
#         }
#     }

#     response = client.post("/tasks/create", json=request)
#     print(response.json())

#     assert response.status_code == 200


# def test_dialogue():
#     """
#     Test making a generator request for a monologue
#     """
    
#     request = {
#         "generatorName": "dialogue",
#         "config": {
#             "characterIds": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277"],
#             "prompt": "Debate whether or not pizza is a vegetable",
#         }
#     }

#     response = client.post("/tasks/create", json=request)
#     print(response.json())

#     assert response.status_code == 200


# def test_story():
#     """
#     Test making a generator request for stories
#     """
    
#     request = {
#         "generatorName": "story",
#         "config": {
#             "characterIds": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277", "6598e103dd06d165264f2247", "6598ee16dd06d16526503ce7"],
#             "prompt": "The four protagonists wake up suddenly, inside of a cube-shaped chamber with 6 hatches on each wall. They have no memory of how they got there, and no idea how to escape.",
#         }
#     }

#     response = client.post("/tasks/create", json=request)
#     print(response.json())

#     assert response.status_code == 200



def test_littlemartians():
    """
    Test making a generator request for Little Martians posters
    """
    
    request = {
        "generatorName": "littlemartians",
        "config": {
            "martian": "Verdelis",
            "genre": "Drama",
            "setting": "Human Imaginarium",
            "aspect_ratio": "portrait",
            "prompt": "Verdelis won the lottery",
        }
    }

    response = client.post("/tasks/create", json=request)
    print(response.json())

    assert response.status_code == 200
