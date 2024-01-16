import os
import requests
import tempfile

from .. import utils
from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..scenarios import story
from ..models import StoryRequest, StoryResult
from .animation import screenplay_clip

MAX_PIXELS = 1024 * 1024
MAX_WORKERS = 3


def animated_story(request: StoryRequest):
    screenplay = story(request)
    print(screenplay)

    characters = {
        character_id: EdenCharacter(character_id) 
        for character_id in request.character_ids + [request.narrator_id]
    }

    character_name_lookup = {
        character.name: character_id
        for character_id, character in characters.items()
    }

    images = [
        characters[character_id].image 
        for character_id in request.character_ids
    ]

    width, height = utils.calculate_target_dimensions(images, MAX_PIXELS)

    def run_story_segment(clip):
        if clip['voiceover'] == 'character':
            character_id = character_name_lookup[clip['character']]
            character = characters[character_id]
        else:
            character = characters[request.narrator_id]
        output_filename, thumbnail_url = screenplay_clip(
            character,
            clip['speech'],
            clip['image_description'],
            width,
            height
        )
        return output_filename, thumbnail_url

    results = utils.process_in_parallel(
        screenplay['clips'], 
        run_story_segment,
        max_workers=MAX_WORKERS
    )

    video_files = [video_file for video_file, thumbnail in results]
    thumbnail_url = results[0][1]

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        utils.concatenate_videos(video_files, temp_output_file.name)
        with open(temp_output_file.name, 'rb') as f:
            video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")

    # clean up clips
    for video_file in video_files:
        os.remove(video_file)

    return output_url, thumbnail_url
