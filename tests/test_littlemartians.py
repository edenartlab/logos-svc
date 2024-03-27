import random
from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_little_martians():
    """
    Test Little Martian illustration on static character and prompt
    """

    for z in range(1):

        martians = ["Kweku", "Kalama", "Shuijing", "Mycos", "Verdelis", "Ada"]
        settings = ["Human Imaginarium", "Physical Reality"]
        genres = ["Drama", "Comedy", "Horror", "Action", "Mystery"]
        aspect_ratios = ["portrait", "landscape", "square"]
        prompts = [
            "is feeling mischievous",
            "is doing high end machine learning research on finetuning multimodal diffusion models",
            "feels lonely",
            "just won the lottery",
            "is feeling nostalgic",
            "meets a goblin",
            "is going on an adventure",
            "is living for 5000 years",
            "is still making investments while living 50000 years into the future",
            "is living on Mars",
            "is in a desert camp near the Greater Niland California Prosperity Sphere",
            "is living in Slab City",
            "you find a genie lamp in the sand",
            "working on a math problem set",
            "gets abducted by aliens",
            "is living in the post-apocalypse",
            "wondering about utopia",
            "just read Three Body Problem for the first time",
            "deconstructing Nietszche",
            "going to the toilet",
            "world renowned mathematician",
            "tripping on LSD",
            "time traveler from the future",
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
        response = client.post("/kojii/va2rosa", json=request)
        print(response.json())

        import requests
        from io import BytesIO
        from PIL import Image

        uri, _ = response.json()
        response = requests.get(uri)
        img = Image.open(BytesIO(response.content))
        filename = f"{martian} - {setting} - {genre} - {prompt[0:30]}"
        img.save(f"tests/martians/{filename}.jpg")

    assert response.status_code == 200
