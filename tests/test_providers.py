from app.plugins import replicate, elevenlabs, s3

def test_elevenlabs():
    """
    Test Elevenlabs API
    """
    text = "Hi"
    voice = "21m00Tcm4TlvDq8ikWAM"

    audio_bytes = elevenlabs.tts(text, voice)

    assert len(audio_bytes) > 0
    

