import random
from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)

def test_little_martians():
    """
    Test Little Martian illustration on static character and prompt
    """

    martians = ["Kweku", "Kalama", "Shuijing", "Mycos", "Verdelis", "Ada"]
    settings = ["Human Imaginarium", "Physical Reality"]
    genres = ["Drama", "Comedy", "Horror", "Action", "Mystery"]
    aspect_ratios = ["portrait", "landscape", "square"]
    prompts = [
        "is feeling mischievous", 
        "is doing high end machine learning research on finetuning multimodal diffusion models", 
        "feels lonely",
        "just won the lottery",
        "is living for 5000 years",
        "is still making investments while living 50000 years into the future",
        "is living on Mars",
        "is in a desert camp near the Greater Niland California Prosperity Sphere",
        "is living in Slab City"
    ]

    martian = random.choice(martians)
    setting = random.choice(settings)
    genre = random.choice(genres)
    prompt = random.choice(prompts)
    aspect_ratio = random.choice(aspect_ratios)

    request = {
        "martian": martian,
        "prompt": prompt,
        "setting": setting,
        "genre": genre,
        "aspect_ratio": aspect_ratio,
    }
    print(request)
    response = client.post("/animation/little_martian", json=request)
    print(response.json())

    assert response.status_code == 200
