from enum import Enum
from typing import Optional, List
from fastapi import APIRouter
from typing import List, Optional
from pydantic import Field, BaseModel, ValidationError

import requests
import tempfile

from ..mongo import get_character_data
from ..llm import LLM
from ..utils import calculate_target_dimensions, concatenate_videos, combine_speech_video
from ..models import CinemaRequest, CinemaResult
from ..prompt_templates.cinema import (
    screenwriter_system_template,
    screenwriter_prompt_template,
    director_template,
    cinematographer_template,
)
from ..plugins import replicate, elevenlabs, s3, eden
from ..character import EdenCharacter
from .dags import talking_head

print("ok 1")
print(talking_head)
MAX_PIXELS = 1024 * 1024


router = APIRouter()


import subprocess

def combine_audio_video22(audio_url: str, video_url: str, output_filename: str):
    command = f'ffmpeg -stream_loop -1 -i "{video_url}" -i "{audio_url}" -shortest -y "{output_filename}"'
    subprocess.run(command, shell=True, check=True)

import subprocess
import os
import tempfile

def combine_audio_video(audio_url: str, video_url: str):
    # Create temporary files
    audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=True)
    video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=True)
    output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)

    # Download the files
    os.system(f"wget -O {audio_file.name} {audio_url}")
    os.system(f"wget -O {video_file.name} {video_url}")

    # Get the duration of the audio file
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_file.name}"
    audio_duration = subprocess.check_output(cmd, shell=True).decode().strip()

    # Loop the video
    looped_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=True)
    cmd = f"ffmpeg -y -stream_loop -1 -i {video_file.name} -c copy -t {audio_duration} {looped_video.name}"
    subprocess.run(cmd, shell=True)

    # Merge the audio and the looped video
    cmd = f"ffmpeg -y -i {looped_video.name} -i {audio_file.name} -c:v copy -c:a aac -strict experimental -shortest {output_file.name}"
    subprocess.run(cmd, shell=True)

    # Return the name of the output file
    return output_file.name

class VoiceoverMode(Enum):
    character = 'character'
    narrator = 'narrator'
    none = 'none'
    
class Clip(BaseModel):
    """
    A single clip in a screenplay sequence
    """
    voiceover: VoiceoverMode = Field(description="Voiceover mode for clip")
    character: Optional[str] = Field(description="Character name if voiceover mode is character, otherwise null")
    speech: str = Field(description="Spoken text for clip")
    image_description: str = Field(description="Image for clip, or possibly just of narrator in some scene")

class Screenplay(BaseModel):
    """
    A screenplay consisting of a sequence of clips
    """
    clips: List[Clip] = Field(description="Clips in the sequence")


@router.post("/story/cinema")
def cinema(request: CinemaRequest):
    params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

    print("ok")

#     files = ['/Users/genekogan/eden/edenartlab/logos-svc/thisisthevideo2.mp4', '/var/folders/kj/0_ly06kx2_1cq24q67mnns_00000gn/T/tmpw7jwu6a8.mp4', '/var/folders/kj/0_ly06kx2_1cq24q67mnns_00000gn/T/tmpiei1qihj.mp4', '/var/folders/kj/0_ly06kx2_1cq24q67mnns_00000gn/T/tmpf58ym23z.mp4']

#     print(files)
# #    concatenate_videos(files, "myoutput234.mp4")



#     audio_url = "https://edenartlab-dev.s3.amazonaws.com/077bb727a4d0cdb3c8789f2b208e1c36b68858e3a62e6ac8a779adc68b1a52a5.mp3"
#     video_url = "https://replicate.delivery/pbxt/0ccL45e9IiW1HaItJZq5mw4dyfXwhWJUWUJegVIMfcV7QOpIB/txt2vid_00001.mp4"

#     output_filename = "thisisthevideo21.mp4"
#     output_filename = combine_audio_video(audio_url, video_url)
#     print(output_filename)

#     return
    
    characters = {
        character_id: EdenCharacter(character_id) 
        for character_id in request.character_ids
    }

    # hack: add narrator
    characters["657926f90a0f725740a93b77"] = EdenCharacter("657926f90a0f725740a93b77")


    character_name_lookup = {
        character.name: character_id
        for character_id, character in characters.items()
    }

    images = [
        characters[character_id].image 
        for character_id in request.character_ids
    ]

    width, height = calculate_target_dimensions(images, MAX_PIXELS)

    screenwriter = LLM(
        model=request.model,
        system_message=str(screenwriter_system_template),
        params=params,
    )

    character_details = ""
    for character_id in request.character_ids:
        character = characters[character_id]
        character_detail = f"""---
    Name: {character.name}
    Description: {character.identity}
    
    """
        character_details += character_detail

    prompt = screenwriter_prompt_template.substitute(
        character_details=character_details,
        story=request.prompt,
    )
    print("prompt", prompt)


    story = screenwriter(prompt, output_schema=Screenplay)
    # story = {'clips': [{'voiceover': 'narrator', 'character': None, 'speech': 'In the depths of an enigmatic cube-shaped chamber, cloaked in shadows, four strangers awaken. Confusion and urgency are etched upon their faces, for not one recalls how they came to be ensnared within this perplexing contraption.', 'image_description': 'A shadowy, mysterious cube-shaped chamber with eerie lighting.'}, {'voiceover': 'character', 'character': 'Orion Blackwood', 'speech': "As the echoes of our disoriented murmurs fade, I can't help but wonder... Is this yet another grand illusion, or a dire predicament we must escape from?", 'image_description': 'Orion Blackwood looking around, his face a mixture of curiosity and concern.'}, {'voiceover': 'character', 'character': 'Elara Vexley', 'speech': "Illusion or not, we must rely on more than just tricks to navigate our way out. Let's assess our surroundings for any clues. The stars have always guided me; perhaps they hold answers here too.", 'image_description': 'Elara Vexley examining the walls of the chamber with a resolute gaze.'}, {'voiceover': 'character', 'character': 'Dr. Silas Quill', 'speech': 'A curious puzzle indeed. If we are to unlock the secrets of this place, we must think like the cryptographer, deciphering the hidden within the apparent. Let us search for patterns.', 'image_description': 'Dr. Silas Quill scrutinizing the chamber with a contemplative look.'}, {'voiceover': 'character', 'character': 'Kaelin', 'speech': 'The walls may not speak in whispers like the forest, but I trust they conceal vital truths. Our escape may lie in understanding the nature of our confinement.', 'image_description': "Kaelin running her fingers along the chamber's walls, as if communicating with them."}]}
    print(story)


    all_clips = []

    for clip in story['clips']:
        
        if clip['voiceover'] == 'character':
            character_id = character_name_lookup[clip['character']]
            character = characters[character_id]
            output = talking_head(
                character, 
                clip['speech'],
                width,
                height,
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                response = requests.get(output, stream=True)
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file.flush()
            
            #all_clips.append(output)
            all_clips.append(temp_file.name)
            
        elif clip['voiceover'] == 'narrator':
            character_id = "657926f90a0f725740a93b77" #character_name_lookup['Orion Blackwood']
            character = characters[character_id]
            # output = talking_head(
            #     character, 
            #     clip['speech'],
            #     width,
            #     height,
            # )
            # all_clips.append(output)
            
            
            audio_bytes = elevenlabs.generate(
                clip['speech'], 
                voice=character.voice
            )
            audio_url = s3.upload(audio_bytes, "mp3")
            video_url = replicate.txt2vid(
                interpolation_texts=[clip['image_description']],
                width=width,
                height=height,
            )
            print("AUD", audio_url, video_url)

            # audio_url = "https://edenartlab-dev.s3.amazonaws.com/077bb727a4d0cdb3c8789f2b208e1c36b68858e3a62e6ac8a779adc68b1a52a5.mp3"
            # video_url = "https://replicate.delivery/pbxt/0ccL45e9IiW1HaItJZq5mw4dyfXwhWJUWUJegVIMfcV7QOpIB/txt2vid_00001.mp4"

            #output_filename = "thisisthevideo.mp4"
            output_filename = combine_speech_video(audio_url, video_url)
            print(output_filename)

            #output_filename = temp_file.name
            print(output_filename)

            all_clips.append(output_filename)

        else:
            output = replicate.txt2vid(
                interpolation_texts=[clip['image_description']],
                width=width,
                height=height,
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                response = requests.get(output, stream=True)
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file.flush()
            
            #all_clips.append(output)
            all_clips.append(temp_file.name)
            

    # print("THE URLS")
    # all_clips = ['/Users/genekogan/eden/edenartlab/logos-svc/thisisthevideo.mp4', '/var/folders/kj/0_ly06kx2_1cq24q67mnns_00000gn/T/tmpw7jwu6a8.mp4', '/var/folders/kj/0_ly06kx2_1cq24q67mnns_00000gn/T/tmpiei1qihj.mp4', '/var/folders/kj/0_ly06kx2_1cq24q67mnns_00000gn/T/tmpf58ym23z.mp4']
    
    print(all_clips)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output_file:
        concatenate_videos(all_clips, temp_output_file.name)
        with open(temp_output_file.name, 'rb') as f:
            video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")
        print("OUTPUT", output_url)
        
        # copy temp_output_file.name to output file in root dir
        filename = temp_output_file.name.split("/")[-1]
        print("FILENAME", filename)
        os.system(f"cp {temp_output_file.name} new_{filename}")



        
        os.remove(temp_output_file.name)
        for clip in all_clips:
            os.remove(clip)
    # screenwriter_message = str(screenwriter_template)
    # director_message = str(director_template)
    # cinematographer_message = str(cinematographer_template)

    # screenwriter = LLM(
    #     model=request.model,
    #     system_message=screenwriter_message,
    #     params=params,
    # )
    # director = LLM(
    #     model=request.model,
    #     system_message=director_message,
    #     params=params,
    # )
    # cinematographer = LLM(
    #     model=request.model,
    #     system_message=cinematographer_message,
    #     params=params,
    # )

    # story = screenwriter(request.prompt)
    # stills = director(story)
    # design = cinematographer(stills)

    # stills = text_to_lines(stills) 
    
    # result = CinemaResult(stills=stills)

    return CinemaResult(stills=["TBD"])


class ComicRequest(BaseModel):
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}

class ComicResult(BaseModel):
    comic: List[str]

@router.post("/story/comic")
def comic(request: ComicRequest):
    print("TBD comic")
    result = ComicResult(comic=["TBD"])
    return result
