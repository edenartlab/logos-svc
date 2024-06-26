import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class Climate(Enum):
    arid = "arid"
    temperate = "temperate"
    tropical = "tropical"
    alpine = "alpine"
    cold = "cold"
    warm = "warm"
    humid = "humid"
    dry = "dry"
    mediterranean = "mediterranean"
    oceanic = "oceanic"
    continental = "continental"
    polar = "polar"
    subtropical = "subtropical"
    desert = "desert"
    savanna = "savanna"
    rainforest = "rainforest"
    tundra = "tundra"
    monsoon = "monsoon"
    steppe = "steppe"


class Landform(Enum):
    mountains = "mountains"
    valleys = "valleys"
    plateaus = "plateaus"
    hills = "hills"
    plains = "plains"
    dunes = "dunes"
    canyons = "canyons"
    cliffs = "cliffs"
    caves = "caves"
    volcanoes = "volcanoes"
    rivers = "rivers"
    lakes = "lakes"
    glaciers = "icebergs"
    fjords = "fjords"
    deltas = "deltas"
    estuaries = "estuaries"
    wetlands = "wetlands"
    deserts = "deserts"
    craters = "craters"
    atolls = "atolls"
    peninsula = "peninsula"
    islands = "island surrounder by water"
    basins = "basins"
    gorges = "gorges"
    waterfalls = "waterfalls"
    rift_valleys = "rift valleys"
    lava_flows = "obsidian lava flows steam"


class BodyOfWater(Enum):
    oceans = "oceans"
    seas = "seas"
    rivers = "rivers"
    lakes = "lakes"
    ponds = "ponds"
    streams = "streams"
    creeks = "creeks"
    estuaries = "estuaries"
    bays = "bays"
    gulfs = "gulfs"
    lagoons = "lagoons"
    marshes = "marshes"
    swamps = "swamps"
    reservoirs = "reservoirs"
    waterfalls = "waterfalls"
    glacial_lakes = "glacial lakes"
    wetlands = "wetlands"
    springs = "springs"
    brooks = "brooks"


class Structure(Enum):
    bridges = "small bridges"
    tunnels = "small tunnels"
    dams = "small dams"
    skyscrapers = "small skyscrapers"
    castles = "small castles"
    temples = "small temples"
    churches = "small churches"
    mosques = "small mosques"
    fortresses = "small fortresses"
    monuments = "small monuments"
    statues = "small statues"
    towers = "small towers"
    silos = "small silos"
    industrial_factories = "small industrial factories"
    piers = "small piers"
    harbors = "small harbors"


class Season(Enum):
    spring = "spring"
    summer = "summer"
    autumn = "autumn"
    winter = "winter"
    rainy = "rainy"
    sunny = "sunny"
    clouds_from_above = "clouds from above"
    stormy_clouds_from_above = "stormy clouds from above"
    foggy_mist = "foggy mist"
    snowy = "snowy"
    windy = "windy"
    humid = "humid"
    dry = "dry"
    hot = "hot"
    cold = "cold"
    mild = "mild"
    freezing = "freezing"
    hail = "hail"
    sleet = "sleet"
    blizzard = "blizzard"
    heatwave = "heatwave"
    drought = "drought"


# class TimeOfDay(Enum):
#     dawn = "dawn"
#     morning = "morning"
#     noon = "noon"
#     afternoon = "afternoon"
#     dusk = "dusk"
#     evening = "evening"
#     sunset = "sunset"


class Color(Enum):
    monochromatic = "monochromatic"
    analogous = "analogous"
    complementary = "complementary"
    split_complementary = "split-complementary"
    triadic = "triadic"
    tetradic = "tetradic"
    square = "square"
    neutral = "neutral"
    pastel = "pastel"
    warm = "warm"
    cool = "cool"
    vibrant = "vibrant"
    muted = "muted"
    earth_tones = "earth tones"
    jewel_tones = "jewel tones"
    metallic = "metallic"


class KojiiHueminRequest(BaseModel):
    """
    A request for Huemin endpoint
    """

    climate: Climate
    landform: Landform
    body_of_water: BodyOfWater
    # structure: Structure
    # season: Season
    # time_of_day: TimeOfDay
    # color: Color
    seed: Optional[int] = Field(default=None, description="Random seed")


def generate_prompt(selected_climate, selected_landform, selected_body_of_water):
    base_prompt = "isometric generative landscape orthographic abstract aj casson perlin noise 3d shaders areal embroidery minimalism claude monet oil painting pastel"

    selected_structure = (
        random.choice(list(Structure)).value if random.random() < 0.20 else ""
    )
    selected_season = (
        random.choice(list(Season)).value if random.random() < 0.95 else ""
    )
    # selected_time_of_day = random.choice(list(TimeOfDay)).value
    selected_colors = random.choice(list(Color)).value if random.random() < 0.95 else ""

    selected_keywords = [
        selected_climate.value,
        selected_landform.value,
        selected_body_of_water.value,
        selected_structure,
        selected_season,
        # selected_time_of_day,
        selected_colors,
    ]
    landscape_keywords = " ".join(selected_keywords)

    prompt = base_prompt + " (((" + landscape_keywords + ")))"
    return prompt


def kojii_huemin(request: KojiiHueminRequest, callback=None):
    prompt = generate_prompt(request.climate, request.landform, request.body_of_water)
    seed = request.seed if request.seed else random.randint(0, 1000000)
    uc_text = ["blurry bad dull green", "blurry bad dull"][random.randint(0, 1)]

    print("HUEMIN REQUEST")
    print(request)
    print(prompt)

    config = {
        "mode": "kojii/huemin",
        "text_input": prompt,
        "uc_text": uc_text,
        "seed": seed,
    }

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url
