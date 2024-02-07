import os
import requests
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

from .. import utils
from .animation import talking_head
from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..scenarios import dialogue
from ..models import DialogueRequest

MAX_PIXELS = 1024 * 1024
MAX_WORKERS = 3


def animated_dialogue(request: DialogueRequest):
    result = dialogue(request)
    print(result)
    
    characters = {
        character_id: EdenCharacter(character_id) 
        for character_id in request.character_ids
    }
    images = [
        characters[character_id].image 
        for character_id in request.character_ids
    ]
    images = list(set(images))
    width, height = utils.calculate_target_dimensions(images, MAX_PIXELS)

    def run_talking_head_segment(message, idx):
        character = characters[message["character_id"]]
        output, _ = talking_head(
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

    video_files = utils.process_in_parallel(
        result.dialogue,
        run_talking_head_segment,
        max_workers=MAX_WORKERS
    )

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
    print("DO IMAGES")
    print(images)
    thumbnail = utils.create_dialogue_thumbnail(*images, width, height)
    thumbnail_url = s3.upload(thumbnail, "webp")

    return output_url, thumbnail_url