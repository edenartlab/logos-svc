import requests

from .animation import talking_head
from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..scenarios import monologue
from ..models import MonologueRequest
from ..utils import *


def animated_monologue(request: MonologueRequest, callback=None):
    result = monologue(request)
    
    if callback:
        callback(progress=0.2)
    
    character = EdenCharacter(request.character_id)
    
    output, thumbnail_url = talking_head(
        character, 
        result.monologue, 
        gfpgan=request.gfpgan
    )

    if request.intro_screen:
        image = download_image(character.image)
        width, height = image.size

        text = [
            f"{character.name}: {request.prompt}"
        ]
        intro_screen = video_textbox(
            text, 
            width, 
            height, 
            duration = 8,
            fade_in = 1.5,
            margin_left = 25,
            margin_right = 25
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            response = requests.get(output, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file.flush()
        
        video_files = [intro_screen, temp_file.name]

        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
            concatenate_videos(video_files, temp_output_file.name)
            with open(temp_output_file.name, 'rb') as f:
                video_bytes = f.read()
            output_url = s3.upload(video_bytes, "mp4")
    
    else:
        output_bytes = requests.get(output).content
        output_url = s3.upload(output_bytes, "mp4")
    
    return output_url, thumbnail_url
