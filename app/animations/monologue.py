import requests

from .animation import talking_head
from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..scenarios import monologue
from ..models import MonologueRequest


def animated_monologue(request: MonologueRequest):
    character = EdenCharacter(request.character_id)
    #thumbnail_url = character.image
    result = monologue(request)
    output, thumbnail_url = talking_head(character, result.monologue)
    output_bytes = requests.get(output).content
    output_url = s3.upload(output_bytes, "mp4")
    return output_url, thumbnail_url
