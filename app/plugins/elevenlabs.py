import io
import os
import random
import wave
from elevenlabs import generate, set_api_key, Voice, VoiceSettings, play

from ..utils import exponential_backoff

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

set_api_key(ELEVENLABS_API_KEY)

male_voices = ['29vD33N1CtxCmqQRPOHJ', '2EiwWnXFnvU5JabPnv8n', '5Q0t7uMcjvnagumLfvZi', 'CYw3kZ02Hs0563khs1Fj', 'D38z5RcWu1voky8WS1ja', 'ErXwobaYiN019PkySvjV', 'GBv7mTt0atIp3Br8iCZE', 'IKne3meq5aSn9XLyUdCD', 'JBFqnCBsd6RMkjVDRZzb', 'N2lVS1w4EtoT3dr4eOWO', 'ODq5zmih8GrVes37Dizd', 'SOYHLrjzK2X1ezoPC6cr', 'TX3LPaxmHKxFdv7VOQHJ', 'TxGEqnHWrfWFTfGW9XjX', 'VR6AewLTigWG4xSOukaG', 'Yko7PKHZNXotIFUBG7I9', 'ZQe5CZNOzWyzPSCn5a3c', 'Zlb1dXrM653N07WRdFW3', 'bVMeCyTHy58xNoL34h3p', 'flq6f7yk4E4fJM5XTYuZ', 'g5CIjZEefAph4nQFvHAz', 'onwK4e9ZLuTAKqWW03F9', 'pNInz6obpgDQGcFmaJgB', 'pqHfZKP75CvOlQylNhV4', 't0jbNlBVZ17f02VDIeMI', 'wViXBPUzp2ZZixB1xQuM', 'yoZ06aMxZJJ28mfd3POQ', 'zcAOhNBS3c14rBihAFp1']

female_voices = ['21m00Tcm4TlvDq8ikWAM', 'AZnzlk1XvdvUeBnXmlld', 'EXAVITQu4vr4xnSDxMaL', 'LcfcDJNUP1GQjkzn1xUU', 'MF3mGyEYCl7XYWbV9V6O', 'ThT5KcBeYPX3keUQqHPh', 'XB0fDUnXU5powFXDhCwa', 'XrExE9yKIg1WjnnlVkGX', 'pFZP5JQG7iQjIQuC4Bku', 'jBpfuIE2acCO8z3wKNLl', 'jsCqWAovK2LkecY7zXl4', 'oWAxZDx7w5VEj9dCyTzz', 'pMsXgVXv3BLzUgSXRplE', 'piTKgcLEGmPE4e6mEKli', 'z9fAnlkpzviPz146aGWa', 'zrHiDhphv9ZnVXBqCLjz']


def tts(
    text: str, 
    voice: str,
    max_attempts: int = 6,
    initial_delay: int = 5,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.35,
    use_speaker_boost: bool = True
):
    def generate_with_params():
        return generate(
            text=text, 
            voice=Voice(
                voice_id=voice,
                settings=VoiceSettings(
                    stability=stability, 
                    similarity_boost=similarity_boost, 
                    style=style, 
                    use_speaker_boost=use_speaker_boost
                )
            )
        )

    audio_bytes = exponential_backoff(
        generate_with_params, 
        max_attempts=max_attempts, 
        initial_delay=initial_delay
    )

    return audio_bytes


def get_random_voice(gender: str = None):
    if gender and gender not in ["male", "female"]:
        raise ValueError
    
    if gender == "male":
        voices = male_voices
    elif gender == "female":
        voices = female_voices
    else:
        voices = male_voices + female_voices
    
    return random.choice(voices)
