import os
from elevenlabs import generate, set_api_key
from ..utils import exponential_backoff

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

set_api_key(ELEVENLABS_API_KEY)


def tts(
    text: str, 
    voice: str,
    max_attempts: int = 6,
    initial_delay: int = 5,
):
    def generate_with_params():
        return generate(text, voice=voice)

    audio_bytes = exponential_backoff(
        generate_with_params, 
        max_attempts=max_attempts, 
        initial_delay=initial_delay
    )

    return audio_bytes