from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_summary():
    """
    Test summarization of a document
    """
    from app.prompt_templates.assistant import creator_template
    text = creator_template.substitute(name="Eden", identity="")
    
    request = {
        "text": text
    }

    response = client.post("/tasks/summary", json=request)
    print(response.json())

    assert response.status_code == 200


def test_moderation():
    """
    Test moderation of some text
    """    
    request = {
        "text": "this is safe text"
    }

    response = client.post("/tasks/moderation", json=request)
    print(response.json())

    assert response.status_code == 200
