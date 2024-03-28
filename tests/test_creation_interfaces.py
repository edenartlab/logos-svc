import random
from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


def test_kojii_makeitrad():
    """
    Test Makeitrad
    """

    request = {
        "setting": random.choice(["inside", "outside"]),
        "location": random.choice(
            [
                "jungle",
                "cliff front",
                "desert",
                "redwood forest",
                "city suburbia",
                "montana mountains",
                "green hills",
            ],
        ),
        "time": random.choice(["noon", "dawn", "red sunset", "night"]),
        "color": random.choice(
            ["default", "orange", "yellow/green", "light blue", "light pink"],
        ),
        "clouds": random.choice([True, False]),
        "pool": random.choice([True, False]),
        "aspect_ratio": random.choice(["portrait", "landscape", "square"]),
    }
    response = client.post("/kojii/makeitrad", json=request)
    print(response.json())

    assert response.status_code == 200


def test_kojii_chebel():
    """
    Test Chebel
    """

    request = {
        "number": random.choice(["one", "many"]),
        "aspect_ratio": random.choice(["portrait", "landscape"]),
        "abstract": random.uniform(0, 1),
        "color": random.choice(["color", "black and white"]),
    }
    response = client.post("/kojii/chebel", json=request)
    print(response.json())

    assert response.status_code == 200


def test_kojii_untitledxyz():
    """
    Test Untitledxyz
    """

    request = {
        "type": random.choice(["column", "context"]),
        "human_machine_nature": random.uniform(0, 1),
    }

    request = {"type": "column", "human_machine_nature": 0.5}

    response = client.post("/kojii/untitledxyz", json=request)
    print(response.json())

    assert response.status_code == 200


def test_kojii_violetforest():
    """
    Test Violetforest
    """

    request = {
        "cybertwee_cyberpunk": random.uniform(0, 1),
        "style": random.choice(["Kawaii", "Stars", "Lace", "Flowers"]),
    }

    response = client.post("/kojii/violetforest", json=request)
    print(response.json())

    assert response.status_code == 200


def test_kojii_huemin():
    """
    Test Huemin
    """

    request = {
        "climate": random.choice(
            [
                "arid",
                "temperate",
                "tropical",
                "alpine",
                "cold",
                "warm",
                "humid",
                "dry",
                "mediterranean",
                "oceanic",
                "continental",
                "polar",
                "subtropical",
                "desert",
                "savanna",
                "rainforest",
                "tundra",
                "monsoon",
                "steppe",
            ],
        ),
        "landform": random.choice(
            [
                "mountains",
                "valleys",
                "plateaus",
                "hills",
                "plains",
                "dunes",
                "canyons",
                "cliffs",
                "caves",
                "volcanoes",
                "rivers",
                "lakes",
                "glaciers",
                "fjords",
                "deltas",
                "estuaries",
                "wetlands",
                "deserts",
                "craters",
                "atolls",
                "peninsula",
                "islands",
                "basins",
                "gorges",
                "waterfalls",
                "rift valleys",
            ],
        ),
        "body_of_water": random.choice(
            [
                "oceans",
                "seas",
                "rivers",
                "lakes",
                "ponds",
                "streams",
                "creeks",
                "estuaries",
                "fjords",
                "bays",
                "gulfs",
                "lagoons",
                "marshes",
                "swamps",
                "reservoirs",
                "waterfalls",
                "glacial lakes",
                "wetlands",
                "springs",
                "brooks",
            ],
        ),
        # "structure": random.choice(["bridges", "tunnels", "dams", "skyscrapers", "castles", "temples", "churches", "mosques", "fortresses", "monuments", "statues", "towers", "silos", "industrial factories", "piers", "harbors"]),
        # "season": random.choice(["spring", "summer", "autumn", "winter", "rainy", "sunny", "cloudy", "stormy clouds", "foggy mist", "snowy", "windy", "humid", "dry", "hot", "cold", "mild", "freezing", "thunderstorms", "hail", "sleet", "blizzard", "heatwave", "drought"]),
        # "time_of_day": random.choice(["", "dawn", "morning", "noon", "afternoon", "dusk", "evening", "sunset"]),
        # "color": random.choice(["monochromatic", "analogous", "complementary", "split-complementary", "triadic", "tetradic", "square", "neutral", "pastel", "warm", "cool", "vibrant", "muted", "earth tones", "jewel tones", "metallic"])
    }

    response = client.post("/kojii/huemin", json=request)
    print(response.json())

    assert response.status_code == 200
