from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_summary():
    """
    Test summarization of a document
    """
    from app.prompt_templates.assistant import creator_template
    text = creator_template.substitute(name="Eden")
    
    request = {
        "text": text
    }

    response = client.post("/summary", json=request)
    print(response.json())

    assert response.status_code == 200
