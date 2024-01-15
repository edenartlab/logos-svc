import os
from io import BytesIO
import requests
import replicate
from typing import Optional, List
from pydantic import BaseModel, Field

REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")


def get_version(replicate_client, model_name: str):
    model = replicate_client.models.get(model_name)
    return model.latest_version.id


def run_task(
    config: dict[any], 
    model_name: str = None, 
    model_version: str = None
):
    r = replicate.Client(api_token=REPLICATE_API_KEY)
    
    if not model_version:
        version = get_version(r, model_name)
        model_version = f"{model_name}:{version}"

    output = r.run(ref=model_version, input=config)

    return output


def submit_task(
    config: dict[any],
    model_name: str = None,
    model_version: str = None,
    webhook: str = None,
    webhook_events_filter: list[str] = None,
):
    r = replicate.Client(api_token=REPLICATE_API_KEY)

    if not model_version:
        model_version = get_version(r, model_name)

    prediction = r.predictions.create(
        version=model_version,
        input=config,
        webhook=webhook,
        webhook_events_filter=webhook_events_filter,
    )
    return prediction

def wav2lip(
    face_url: str,
    speech_url: str,
    gfpgan: Optional[bool] = Field(False),
    gfpgan_upscale: Optional[int] = Field(1),
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    config = {
        "face_url": face_url,
        "speech_url": speech_url,
        "gfpgan": gfpgan,
        "gfpgan_upscale": gfpgan_upscale
    }

    if width:
        config["width"] = width
    if height:
        config["height"] = height

    output = run_task(
        config, 
        model_name="abraham-ai/character"
    )
    
    output = list(output)
    output_url = output[0]["files"][0]

    return output_url


def sdxl(
    text_input: str,
    width: int,
    height: int,
):
    config = {
        "text_input": text_input,
        "width": width,
        "height": height,
        "n_samples": 1,
    }

    output = run_task(
        config, 
        model_name="abraham-ai/eden-sd-pipelines-sdxl"
    )
    
    output = list(output)
    output_url = output[0]["files"][0]
    
    return output_url


def txt2vid(
    interpolation_texts: List[str],
    width: int,
    height: int,
):
    interpolation_texts = "|".join(interpolation_texts)

    config = {
        "mode": "comfy_txt2vid",
        "interpolation_texts": interpolation_texts,
        "width": width/2,
        "height": height/2,
        "n_frames": 100,
    }

    print("LETS RUN!!!", config)

    output = run_task(
        config, 
        model_name="abraham-ai/eden-comfyui"
    )
    
    output = list(output)
    output_url = output[0]["files"][0]
    
    return output_url