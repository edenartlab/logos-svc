import os
import uuid
import elevenlabs
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from typing import Optional, List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from .scenario import monologue, dialogue
from ..plugins import replicate, elevenlabs, s3

router = APIRouter()


class MonologueRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


@router.post("/dags/monologue")
async def monologue_dag(request: MonologueRequest):
    # result = await monologue(request)
    result = {"prompt": "lucy is a dog", "voice": "Adam"}
    print(result)

    prompt = result["prompt"]
    voice = result["voice"]
    image = "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/e79da30c574bb31ede5eb7c04a9b91517ccc8cf0a3e29d4088bdcca9d4ef777b.jpg"

    audio = elevenlabs.generate(prompt, voice=voice)
    audio_url = s3.upload(audio, "test.mp3")

    config = {
        "face_url": image,
        "speech_url": audio_url,
        "gfpgan": False,
        "gfpgan_upscale": 1,
    }

    # output = run_replicate_task(w2l_config, model_name=CHARACTER_GENERATOR)

    #     out_list = list(output)
    #     outfile_url = out_list[0]["files"][0]
    print(replicate)
    print(replicate.run_task)
    print("GO 2!")
    output = replicate.wav2lip(config)
    print(output)

    output_url = s3.upload(output, "test.mp4")
    print(output_url)


class DialogueRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


@router.post("/dags/dialogue")
async def dialogue_dag(request: DialogueRequest):
    print("DIA")
    print(request)
