import os
import requests
import tempfile
from pydub import AudioSegment

from .. import utils
from ..plugins import replicate, elevenlabs, s3
from ..character import Character, EdenCharacter
from ..scenarios import story
from ..models import StoryRequest
from .animation import screenplay_clip

MAX_WORKERS = 3
INTRO_SCREEN_DURATION = 10


def animated_story(request: StoryRequest, callback=None):
    screenplay = story(request)
    
    music_prompt = screenplay.get("music_prompt")

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
            character, clip["speech"], clip["image_prompt"], width, height
        )
        progress += progress_increment
        if callback:
            callback(progress=progress)
        return output_filename, thumbnail_url

    results = utils.process_in_parallel(
        screenplay["clips"], run_story_segment, max_workers=MAX_WORKERS
    )


    print(":TH RESULTS")
    print(results)

    video_files = [video_file for video_file, thumbnail in results]
    thumbnail_url = results[0][1]

    if request.intro_screen:
        character_names = [characters[character_id].name for character_id in request.character_ids]
        character_name_str = ", ".join(character_names)
        paragraphs = [
            request.prompt,
            f"Characters: {character_name_str}" if character_names else "",
        ]
        intro_screen = utils.video_textbox(
            paragraphs, 
            width, 
            height, 
            duration = INTRO_SCREEN_DURATION,
            fade_in = 2,
            margin_left = 25,
            margin_right = 25
        )
        video_files = [intro_screen] + video_files


    print("T?he VIDEO FILES")
    print(video_files)

    audio_file = None
    if music_prompt:
        print("get audio")
        duration = sum([utils.get_video_duration(video_file) for video_file in video_files])
            
        print("full dur", duration)
        print("the music prompt", music_prompt)
        music_url, _ = replicate.audiocraft(
            prompt=music_prompt,
            seconds=duration
        )
        print(music_url)

        response = requests.get(music_url)
        response.raise_for_status()
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_file.write(response.content)
        audio_file.flush()

        if request.intro_screen:
            silence = AudioSegment.silent(duration=INTRO_SCREEN_DURATION * 1000)
            music = AudioSegment.from_mp3(audio_file.name)
            music = music - 6
            music_with_silence = silence + music.fade_out(5000)
            music_with_silence.export(audio_file.name, format="mp3")

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        utils.concatenate_videos(video_files, temp_output_file.name)
        if audio_file:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file2:
                utils.mix_video_audio(temp_output_file.name, audio_file.name, temp_output_file2.name)                
                with open(temp_output_file2.name, "rb") as f:
                    video_bytes = f.read()
        else:
            with open(temp_output_file.name, "rb") as f:
                video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")

    # clean up clips
    for video_file in video_files:
        os.remove(video_file)

    if audio_file:
        os.remove(audio_file.name)

    if callback:
        callback(progress=0.99)

    return output_url, thumbnail_url
