import os
from io import BytesIO
import requests
import replicate
from typing import Optional
from pydantic import BaseModel, Field

EDEN_API_URL = os.environ.get("EDEN_API_URL")
EDEN_API_KEY = os.environ.get("EDEN_API_KEY")
EDEN_API_SECRET = os.environ.get("EDEN_API_SECRET")

from eden_sdk.EdenClient import EdenClient

eden = EdenClient(
    api_url=EDEN_API_URL,
    api_key=EDEN_API_KEY,
    api_secret=EDEN_API_SECRET,
)

create = eden.create

# def run_task(
#     config: dict[any], 
# ):
#     config = {
#         "text_input": "someone here",
#     }
#     print("GO", config)
#     print("ok 2")
#     urls = eden.create(generator_name='create', config=config)
#     print("ok 3")

#     print(urls[0])
#     print("ok 4")

#     return urls[0]

