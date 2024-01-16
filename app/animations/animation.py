from typing import Optional

from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..utils import combine_speech_video


def talking_head(
    character: EdenCharacter,
    text: str, 
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    audio_bytes = elevenlabs.tts(
        text, 
        voice=character.voice
    )
    audio_url = s3.upload(audio_bytes, "mp3")
    output_url, thumbnail_url = replicate.wav2lip(
        face_url=character.image,
        speech_url=audio_url,
        gfpgan=False,
        gfpgan_upscale=1,
        width=width,
        height=height,
    )
    return output_url, thumbnail_url


def screenplay_clip(
    character: EdenCharacter,
    speech: str,
    image_text: str,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    audio_bytes = elevenlabs.tts(
        speech, 
        voice=character.voice
    )
    audio_url = s3.upload(audio_bytes, "mp3")
    video_url, thumbnail_url = replicate.txt2vid(
        interpolation_texts=[image_text],
        width=width,
        height=height,
    )
    output_filename = combine_speech_video(audio_url, video_url)
    return output_filename, thumbnail_url