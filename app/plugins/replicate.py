import os
from io import BytesIO
import requests
import replicate
from typing import Optional
from pydantic import BaseModel, Field

REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


def get_version(replicate_client, model_name: str):
    model = replicate_client.models.get(model_name)
    return model.latest_version.id


def run_task(
    input: dict[any], 
    model_name: str = None, 
    model_version: str = None
):
    r = replicate.Client(api_token=REPLICATE_API_KEY)
    
    if not model_version:
        version = get_version(r, model_name)
        model_version = f"{model_name}:{version}"

    output = r.run(ref=model_version, input=input)

    return output


def submit_task(
    input: dict[any],
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
        input=input,
        webhook=webhook,
        webhook_events_filter=webhook_events_filter,
    )
    return prediction


class Wav2LipConfig(BaseModel):
    face_url: str
    speech_url: str
    gfpgan: Optional[bool] = Field(False)
    gfpgan_upscale: Optional[int] = Field(1)
    

def wav2lip(
    config: Wav2LipConfig
):
    output = run_task(config, model_name="abraham-ai/character")
    output = list(output)
    output_url = output[0]["files"][0]
    response = requests.get(output_url)
    response.raise_for_status()
    return response.content