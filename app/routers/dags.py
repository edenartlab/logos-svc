import os
import uuid
import requests
import elevenlabs
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed

from .scenario import monologue, dialogue
from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..models import MonologueRequest, DialogueRequest
from .. import utils

MAX_PIXELS = 1024 * 1024

router = APIRouter()

def talking_head(
    character: EdenCharacter,
    text: str, 
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    audio_bytes = elevenlabs.generate(
        text, 
        voice=character.voice
    )
    audio_url = s3.upload(audio_bytes, "mp3")
    output = replicate.wav2lip(
        face_url=character.image,
        speech_url=audio_url,
        gfpgan=False,
        gfpgan_upscale=1,
        width=width,
        height=height,
    )
    return output


@router.post("/dags/monologue")
def monologue_dag(request: MonologueRequest):
    character = EdenCharacter(request.character_id)
    thumbnail_url = character.image
    result = monologue(request)
    output = talking_head(character, result.monologue)
    output_bytes = requests.get(output).content
    output_url = s3.upload(output_bytes, "mp4")
    return output_url, thumbnail_url


@router.post("/dags/dialogue")
def dialogue_dag(request: DialogueRequest):
    result = dialogue(request)
    characters = {
        character_id: EdenCharacter(character_id) 
        for character_id in request.character_ids
    }
    images = [
        characters[character_id].image 
        for character_id in request.character_ids
    ]
    width, height = utils.calculate_target_dimensions(images, MAX_PIXELS)

    def run_talking_head_segment(message):
        character = characters[message["character_id"]]
        output = talking_head(
            character, 
            message["message"], 
            width, 
            height
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            response = requests.get(output, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file.flush()
        return temp_file.name

    # process talking head segments in parallel
    video_files = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_message = {
            executor.submit(run_talking_head_segment, message): message 
            for message in result.dialogue
        }
        for future in as_completed(future_to_message):
            video_files.append(future.result())

    # concatenate the final video clips
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output_file:
        utils.concatenate_videos(video_files, temp_output_file.name)
        with open(temp_output_file.name, 'rb') as f:
            video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")
        os.remove(temp_output_file.name)
        for video_file in video_files:
            os.remove(video_file)

    # generate thumbnail
    thumbnail = utils.create_dialogue_thumbnail(*images, width, height)
    thumbnail_url = s3.upload(thumbnail, "webm")

    return output_url, thumbnail_url