from fastapi.testclient import TestClient
from logos.server import app

client = TestClient(app)


def test_monologue_animation():
    """
    Test monologue on static character and prompt
    """
    request = {
        "character_id": "65f35e7f44390ad1df63680e",
        "prompt": "Tell me what you feel about Bombay Beach",
        "gfpgan": True,
        "intro_screen": True,
    }

    response = client.post("/animation/monologue", json=request)
    print(response.json())
    assert response.status_code == 200


def test_dialogue_animation():
    """
    Test monologue on static character and prompt
    """
    request = {
        # "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277"],
        # "prompt": "Debate panspermia vs. abiogenesis",
        "prompt": "Have a rap battle!! Dis each other. Be expressive in your speech! Exclamations, random ALL CAPS, onomatopoeia, etc. Be creative but sharp. Dis each other! You are trying to win this rap battle against each other.",
        "character_ids": ["65ce8995b6124cd312fedb99", "65eea28c730ba08c8c7b6810"],
        "gfpgan": True,
        "intro_screen": True,
        # "dual_view": True
    }

    response = client.post("/animation/dialogue", json=request)
    print(response.json())
    assert response.status_code == 200


def test_story():
    """
    Test story prompt without characters
    """
    request = {
        "character_ids": [],
        "prompt": "A family of Dragons lives in a mystical layer underneath a volcano. The dragons are beautiful, ornately decorated, fire-breathing, creatures. They are brave and wise. The story should just be about them journeying to a bunch of beautiful far away places in nature, and then coming back to their volcano lair. Make sure the image prompts are very short. No more than 5 words.",
        "intro_screen": True,
        # "music_prompt": "a long drum solo with percussions and bongos",
        "music": True,
    }

    response = client.post("/animation/story", json=request)
    print(response.json())
    assert response.status_code == 200


def test_reel():
    """
    Test music reels
    """
    request = {
        "character_ids": [],
        # "prompt": "A jazz woman dancing to some saxophone jazzy show tunes, instrumental",
        "prompt": "A long commercial about a drug called Paradisium. explain its benefits and side effects, and go on and on and on.",
        "intro_screen": True,
        # "narration": "off",
        # "music_prompt": "death metal heavy rock, incomprehensible, gore, screen"
    }

    response = client.post("/animation/reel", json=request)
    print(response.json())
    assert response.status_code == 200
