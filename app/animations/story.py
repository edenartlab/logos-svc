import os
import requests
import tempfile

from .. import utils
from ..plugins import replicate, elevenlabs, s3
from ..character import Character, EdenCharacter
from ..scenarios import story
from ..models import StoryRequest
from .animation import screenplay_clip

MAX_PIXELS = 1024 * 1024
MAX_WORKERS = 3


def animated_story(request: StoryRequest, callback=None):
    print(request.intro_screen)
    print(request)
    screenplay = story(request)
    screenplay["clips"] = screenplay["clips"]
    if callback:
        callback(progress=0.1)
    print(screenplay)

    characters = {
        character_id: EdenCharacter(character_id)
        for character_id in request.character_ids + [request.narrator_id]
        if character_id != ""
    }

    character_name_lookup = {
        character.name: character_id for character_id, character in characters.items()
    }

    # if any character is new, assign a random voice
    for clip in screenplay['clips']:
        if not clip['character']:
            continue
        character_name = clip['character']
        if character_name not in character_name_lookup:
            characters[character_name] = Character(name=character_name)
            character_name_lookup[character_name] = character_name
        character_id = character_name_lookup[character_name]
        if not characters[character_id].voice:
            voice_id = elevenlabs.get_random_voice()
            characters[character_id].voice = voice_id

    width, height = 1792, 1024

    progress = 0.1
    progress_increment = 0.8 / len(screenplay["clips"])

    def run_story_segment(clip, idx):
        nonlocal progress, progress_increment
        if clip["voiceover"] == "character":
            character_id = character_name_lookup[clip['character']]
            character = characters.get(character_id)
        else:
            character = characters[request.narrator_id]
        output_filename, thumbnail_url = screenplay_clip(
            character, clip["speech"], clip["image_description"], width, height
        )
        progress += progress_increment
        if callback:
            callback(progress=progress)
        return output_filename, thumbnail_url

    results = utils.process_in_parallel(
        screenplay["clips"], run_story_segment, max_workers=MAX_WORKERS
    )

    video_files = [video_file for video_file, thumbnail in results]
    thumbnail_url = results[0][1]

    if request.intro_screen:
        print("LETS GO")
        character_names = [characters[character_id].name for character_id in request.character_ids]
        character_name_str = ", ".join(character_names)
        paragraphs = [
            request.prompt,
            f"Characters: {character_name_str}"
        ]
        intro_screen = utils.video_textbox(
            paragraphs, 
            width, 
            height, 
            duration = 10,
            fade_in = 2,
            margin_left = 25,
            margin_right = 25
        )
        video_files = [intro_screen] + video_files

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        utils.concatenate_videos(video_files, temp_output_file.name)
        with open(temp_output_file.name, "rb") as f:
            video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")

    # clean up clips
    for video_file in video_files:
        os.remove(video_file)

    if callback:
        callback(progress=0.99)

    return output_url, thumbnail_url
