import os
import requests
import tempfile
import random

from .. import utils
from ..plugins import replicate, s3
from ..character import EdenCharacter
from ..llm import LLM
from ..models import LittleMartianRequest, Poster
from .animation import poster
from ..prompt_templates.little_martians import (
    littlemartians_poster_system,
    littlemartians_poster_prompt,
    littlemartians_data,
)


def random_interval(min, max):
    return random.random() * (max - min) + min


def little_martian_poster(request: LittleMartianRequest, callback=None):
    params = {"temperature": 1.0, "max_tokens": 2000, **request.params}

    data = littlemartians_data[request.martian.value][request.setting.value][
        request.genre.value
    ]

    lora = data["lora"]
    character_id = data["character_id"]
    modifier = data["modifier"]
    lora_scale = random_interval(*data["lora_scale"])
    init_image = random.choice(data["init_images"])
    init_image_strength = random_interval(*data["init_image_strength"])
    seed = request.seed if request.seed else random.randint(0, 1000000)

    character = EdenCharacter(character_id)

    littlemartian_writer = LLM(
        model=request.model,
        system_message=littlemartians_poster_system.template,
        params=params,
    )

    prompt = littlemartians_poster_prompt.substitute(
        martian=request.martian.value,
        identity=character.identity,
        setting=request.setting.value,
        genre=request.genre.value,
        premise=request.prompt,
    )

    result = littlemartian_writer(prompt, output_schema=Poster)

    prompt = result["image"]

    text_input = f"{modifier}, {prompt}"

    if request.aspect_ratio == "portrait":
        width, height = 1280, 1920
    elif request.aspect_ratio == "landscape":
        width, height = 1920, 1280
    else:
        width, height = 1600, 1600

    config = {
        "text_input": text_input,
        "lora": lora,
        "lora_scale": lora_scale,
        "init_image": f"https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/{init_image}",
        "init_image_strength": init_image_strength,
        "width": width,
        "height": height,
        "adopt_aspect_from_init_img": False,
        "n_samples": 1,
        "seed": seed,
    }

    image_url, thumbnail_url = replicate.sdxl(config)

    caption = result["caption"]
    print(caption)

    image = utils.download_image(image_url)
    composite_image, thumbnail_image = poster(image, caption)

    img_bytes = utils.PIL_to_bytes(composite_image, ext="JPEG")
    thumbnail_bytes = utils.PIL_to_bytes(thumbnail_image, ext="WEBP")

    output_url = s3.upload(img_bytes, "jpg")
    thumbnail_url = s3.upload(thumbnail_bytes, "webp")

    return output_url, thumbnail_url
