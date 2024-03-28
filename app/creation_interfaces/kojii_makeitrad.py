import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class Setting(Enum):
    inside = "inside"
    outside = "outside"


class Location(Enum):
    jungle = "jungle"
    cliff_front = "cliff front"
    desert = "desert"
    redwood_forest = "redwood forest"
    city_suburbia = "city suburbia"
    montana_mountains = "montana mountains"
    green_hills = "green hills"


class Time(Enum):
    noon = "noon"
    dawn = "dawn"
    red_sunset = "red sunset"
    night = "night"


class Color(Enum):
    default = "default"
    orange = "orange"
    yellow_green = "yellow/green"
    light_blue = "light blue"
    light_pink = "light pink"


class AspectRatio(Enum):
    portrait = "portrait"
    landscape = "landscape"
    square = "square"


class KojiiMakeitradRequest(BaseModel):
    """
    A request for Makeitrad endpoint
    """

    setting: Setting
    location: Location
    time: Time
    color: Color
    clouds: bool
    pool: bool
    aspect_ratio: AspectRatio
    seed: Optional[int] = Field(default=None, description="Random seed")


settings = {"inside": "interior", "outside": "exterior"}

locations = {
    "jungle": "surrounded by overgrown plants, in the lush jungle, large leaves",
    "cliff front": "cliff ocean front overlooking water, tropical plants",
    "desert": "desert (large rock formations:1.5), cactus, succulents and red sands",
    "redwood forest": "in the lush redwood forest with a running river",
    "city suburbia": "urban city suburbia, (house plants) and (outdoor topiaries:1.5)",
    "montana mountains": "dramatic winter snow capped rustic Montana mountains, trees",
    "green hills": "rolling green grass hills and colorful wild flowers",
}

times = {
    "noon": "high noon",
    "dawn": "dawn light with hazy fog",
    "red sunset": "night red sunset",
    "night": "dark black night with large moon and stars",
}

colors = {
    "default": "",
    "orange": "orange accents",
    "yellow/green": "yellow and green accents",
    "light blue": "light blue accents",
    "light pink": "light pink accents",
}

resolutions = {
    "portrait": (768, 1344),
    "landscape": (1344, 768),
    "square": (1024, 1024),
}


def kojii_makeitrad(request: KojiiMakeitradRequest, callback=None):
    setting = settings[request.setting.value]
    location = locations[request.location.value]
    time = times[request.time.value]
    color = colors[request.color.value]
    seed = request.seed if request.seed else random.randint(0, 1000000)

    clouds = "clouds, " if request.clouds else ""
    pool = "(pool:1.5)," if request.pool else ""

    prompt = f"In the style of makeitrad, highly detailed, graphic illustration, almost photorealistic image of an ({setting}:1.5) extra wide angle Landscape mid-century architecture, indoor-outdoor living atrium, {location}, at {time}, {color}, {clouds}{pool} 8k resolution, in the style of midcentury architectural greats. Post and beam, modern glossy, Kodak Portra 100. embedding:makeitrad_embeddings embedding:indoor-outdoor_embeddings"

    neg_pool = "pool, " if not request.pool else ""
    neg_clouds = "clouds, " if not request.clouds else ""

    negative_prompt = f"{neg_pool}{neg_clouds} watermark, text, ugly, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft"

    width, height = resolutions[request.aspect_ratio.value]

    config = {
        "mode": "makeitrad",
        "text_input": prompt,
        "width": width,
        "height": height,
        "n_samples": 1,
        "negative_prompt": negative_prompt,
        "guidance_scale": 7,
        "seed": seed,
    }

    output = replicate.run_task(config, model_name="abraham-ai/eden-comfyui")

    output = list(output)
    image_url = output[0]["files"][0]
    thumbnail_url = output[0]["thumbnails"][0]

    return image_url, thumbnail_url
