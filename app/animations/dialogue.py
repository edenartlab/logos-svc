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


def animated_dialogue(request: DialogueRequest, callback=None):
    print("===== animated_dialogue =====")
    print(request)

    result = dialogue(request)

    print("---")
    print(result)

    if callback:
        callback(progress=0.1)

    characters = {
        character_id: EdenCharacter(character_id)
        for character_id in request.character_ids
    }
    images = [characters[character_id].image for character_id in request.character_ids]

    width, height = utils.calculate_target_dimensions(list(set(images)), MAX_PIXELS)

    progress = 0.1
    progress_increment = 0.8 / len(result.dialogue)

    def run_talking_head_segment(message, idx):
        nonlocal progress, progress_increment
        character = characters[message["character_id"]]
        print(f'run talking head: {message["message"]}')
        output, _ = talking_head(
            character,
            message["message"],
            width,
            height,
            gfpgan=request.gfpgan,
        )
        print(f"output: {output}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            print("download:", output)
            response = requests.get(output, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file.flush()
        progress += progress_increment
        if callback:
            callback(progress=progress)
        print("return temp_file.name:", temp_file.name)
        return temp_file.name

    print("--- run video file tasks ----")

    video_files = utils.process_in_parallel(
        result.dialogue,
        run_talking_head_segment,
        max_workers=MAX_WORKERS,
    )

    print("--- end video file tasks ----")
    print(video_files)

    if request.dual_view:
        print(" -> dual view")
        cropped_images = {}
        for character in characters:
            temp_file = tempfile.NamedTemporaryFile(suffix=".webp", delete=False)
            image = utils.download_image(characters[character].image)
            image = utils.resize_and_crop(image, width, height)
            image.save(temp_file, format="png")
            cropped_images[character] = temp_file.name
        dual_video_files = []
        for idx, (message, video_file) in enumerate(zip(result.dialogue, video_files)):
            opposing_character_id = next(
                c
                for c in characters
                if characters[c].character_id != message["character_id"]
            )
            image = cropped_images[opposing_character_id]
            left = idx % 2 == 0
            video_file = utils.stitch_image_video(image, video_file, left)
            dual_video_files.append(video_file)
        for character in characters:
            os.remove(cropped_images[character])
        for video_file in video_files:
            os.remove(video_file)
        video_files = dual_video_files

    if request.intro_screen:
        print(" -> intro screen")
        character_names = [
            characters[character_id].name for character_id in request.character_ids
        ]
        character_name_str = " and ".join(character_names)
        paragraphs = [request.prompt, f"Dialogue between {character_name_str}"]
        intro_screen = utils.video_textbox(
            paragraphs,
            width * 2 if request.dual_view else width,
            height,
            duration=8,
            fade_in=1.5,
            margin_left=25,
            margin_right=25,  # width + 25
        )
        video_files = [intro_screen] + video_files

    print(video_files)

    # concatenate the final video clips
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        print("concatenate videos")
        utils.concatenate_videos(video_files, temp_output_file.name)
        with open(temp_output_file.name, "rb") as f:
            video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")

    # clean up clips
    for video_file in video_files:
        os.remove(video_file)

    # generate thumbnail
    print("make thumbnail")
    thumbnail = utils.create_dialogue_thumbnail(*images, 2 * width, height)
    thumbnail_url = s3.upload(thumbnail, "webp")
    print("finished thumbnail", thumbnail_url)

    if callback:
        callback(progress=0.99)

    return output_url, thumbnail_url
