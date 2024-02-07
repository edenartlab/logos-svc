import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

# from app.animations.animation import *


import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer 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",
  },
  data=json.dumps({
    "model": "mistralai/mixtral-8x7b-instruct", 
    "messages": [
      {"role": "user", "content": "What is the meaning of life?"}
    ]
  })
)


print(response.json())