import os
import requests
import tempfile
from io import BytesIO
from pydub import AudioSegment

from .. import utils
from ..plugins import replicate, elevenlabs, s3
from ..character import Character, EdenCharacter
from ..scenarios import reel
from ..models import ReelRequest


def animated_reel(request: ReelRequest, callback=None):
    result = reel(request)

    if callback:
        callback(progress=0.1)

    characters = {
        character_id: EdenCharacter(character_id)
        for character_id in request.character_ids + [request.narrator_id]
        if character_id != ""
    }

    character_name_lookup = {
        character.name: character_id for character_id, character in characters.items()
    }

    # if voice is new, assign a random voice
    if result['character']:        
        character_name = result['character']
        if character_name not in character_name_lookup:
            characters[character_name] = Character(name=character_name)
            character_name_lookup[character_name] = character_name
        character_id = character_name_lookup[character_name]
        if not characters[character_id].voice:
            voice_id = elevenlabs.get_random_voice()
            characters[character_id].voice = voice_id

    if request.aspect_ratio == "portrait":
        width, height = 1280, 1920
    elif request.aspect_ratio == "landscape":
        width, height = 1920, 1280
    else:
        width, height = 1600, 1600
        
    min_duration = 20
    speech_audio = None
    duration = min_duration

    if result["speech"]:
        if result["voiceover"] == "character":
            character_id = character_name_lookup[result['character']]
            character = characters.get(character_id)
        else:
            character = characters[request.narrator_id]
        
        if not character:
            voice_id = select_random_voice()
        else:
            if character.voice:
                voice_id = character.voice
            else:
                voice_id = select_random_voice(character)
        
        speech_bytes = elevenlabs.tts(
            result["speech"], 
            voice=voice_id
        )

        speech_file = BytesIO(speech_bytes)
        speech_audio = AudioSegment.from_mp3(speech_file)

        silence1 = AudioSegment.silent(duration=1500)
        silence2 = AudioSegment.silent(duration=2500)
        speech_audio = silence1 + speech_audio + silence2

        duration = max(min_duration, len(speech_audio) / 1000)

    music_url, _ = replicate.audiocraft(
        prompt=result["music_prompt"],
        seconds=duration
    )
    music_bytes = requests.get(music_url).content
    
    if speech_audio:
        buffer = BytesIO()
        music_audio = AudioSegment.from_mp3(BytesIO(music_bytes))
        music_audio = music_audio - 5
        speech_audio = speech_audio + 5  # boost speech

        # combine speech and audio at max duration
        nm, na = len(music_audio), len(speech_audio)
        duration = max(nm, na)
        if len(music_audio) < duration:
            music_audio += AudioSegment.silent(duration=duration - nm)
        elif len(speech_audio) < duration:
            speech_audio += AudioSegment.silent(duration=duration - na)
        combined_audio = music_audio.overlay(speech_audio)

        combined_audio.export(buffer, format="mp3")
        audio_url = s3.upload(buffer.getvalue(), "mp3")
    else:
        audio_url = s3.upload(music_bytes, "mp3")

    video_url, thumbnail_url = replicate.txt2vid(
        interpolation_texts=[result["image_prompt"]],
        width=width,
        height=height,
    )

    print("results", video_url, thumbnail_url, audio_url)

    output_filename = utils.combine_audio_video(audio_url, video_url)

    if callback:
        callback(progress=0.9)

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
            duration = 6,
            fade_in = 1,
            margin_left = 25,
            margin_right = 25
        )
        video_files = [intro_screen, output_filename]

        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
            utils.concatenate_videos(video_files, temp_output_file.name)
            with open(temp_output_file.name, "rb") as f:
                video_bytes = f.read()
            output_url = s3.upload(video_bytes, "mp4")

        # clean up
        for video_file in video_files:
            os.remove(video_file)

    else:
        output_bytes = open(output_filename, "rb").read()
        output_url = s3.upload(output_bytes, "mp4")
        os.remove(output_filename)

    if callback:
        callback(progress=0.99)

    return output_url, thumbnail_url
