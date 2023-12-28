import os
from elevenlabs import *

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
print(ELEVENLABS_API_KEY)

set_api_key(ELEVENLABS_API_KEY)
