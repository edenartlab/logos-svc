import os
from elevenlabs import *

ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY")
print(ELEVEN_API_KEY)

set_api_key(ELEVEN_API_KEY)
