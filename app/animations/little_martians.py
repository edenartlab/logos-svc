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
    littlemartians_data
)

def random_interval(min, max):
    return random.random() * (max - min) + min

def little_martian_poster(request: LittleMartianRequest):
    params = {"temperature": 1.0, "max_tokens": 2000, **request.params}

    data = littlemartians_data[request.martian.value][request.setting.value][request.genre.value]

    lora = data['lora']
    modifier = data['modifier']
    lora_scale = random_interval(*data['lora_scale'])
    init_image = random.choice(data['init_images'])
    init_image_strength = random_interval(*data['init_image_strength'])
    
    
    print("go")


    print(lora)
    print(modifier)
    print(lora_scale)

    
    littlemartian_writer = LLM(
        model=request.model,
        system_message=littlemartians_poster_system.template,
        params=params,
    )
    print("------")
    print(request.prompt)


    prompt = littlemartians_poster_prompt.substitute(
        martian = request.martian.value,
        setting = request.setting.value,
        genre = request.genre.value,
        premise = request.prompt,
    )
    
    
    print(prompt)
    
    result = littlemartian_writer(prompt, output_schema=Poster)

    print(result)
    prompt = result['image']
    

    text_input = f'{modifier}, {prompt}'
    # text_input = f'{modifier}'

    print(text_input)

    # def run_panel(panel, idx):
    #     # pick lora of character
    #     # pick init image character x genre
    print("========")

    if request.aspect_ratio.value == "portrait":
        w, h = 1024, 1280
    elif request.aspect_ratio.value == "landscape":
        w, h = 1280, 768
    elif request.aspect_ratio.value == "square":
        w, h = 1024, 1024



    config = {
        "text_input": text_input,
        "lora": lora,
        "lora_scale": lora_scale,
        "init_image": f'https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/{init_image}',
        "init_image_strength": init_image_strength,
        "width": w,
        "height": h,
        "adopt_aspect_from_init_img": False,
        "n_samples": 1,
    }

    print(config)
    

    image_url, thumbnail_url = replicate.sdxl(config)

    print(image_url, thumbnail_url)

    caption = result['caption']
    print(caption)
    image = utils.download_image(image_url)
    composite_image, thumbnail_image = poster(image, caption)
    # results = utils.process_in_parallel(
    #     comic_book['panels'], 
    #     run_panel,
    #     max_workers=4
    # )

    # image_urls = [image_url for image_url, thumbnail in results]
    # images = [utils.download_image(url) for url in image_urls]
    # captions = [panel['caption'] for panel in comic_book['panels']]

    # composite_image, thumbnail_image = comic_strip(images, captions)
    
    img_bytes = utils.PIL_to_bytes(composite_image, ext="JPEG")
    thumbnail_bytes = utils.PIL_to_bytes(thumbnail_image, ext="WEBP")

    output_url = s3.upload(img_bytes, "jpg")
    thumbnail_url = s3.upload(thumbnail_bytes, "webp")

    return output_url, thumbnail_url
