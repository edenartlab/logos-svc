import os
import uuid
import elevenlabs 
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from typing import Optional, List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from .scenario import monologue, dialogue
from ..plugins import replicate, elevenlabs, s3




router = APIRouter()



# # @task
# # def generate_wav2lip_task(monologue_audio_data: dict, **context):
# #     config = context["dag_run"].conf["config"]

# #     audio_url = monologue_audio_data["url"]
# #     image = config["character"]["image"]
# #     w2l_config = {
# #         "face_url": image,
# #         "speech_url": audio_url,
# #         "gfpgan": False,
# #         "gfpgan_upscale": 1
# #     }

# #     output = run_replicate_task(w2l_config, model_name=CHARACTER_GENERATOR)

# #     out_list = list(output)
# #     outfile_url = out_list[0]["files"][0]
# #     response = requests.get(outfile_url)
# #     response.raise_for_status()
# #     outfile = BytesIO(response.content)
    
# #     taskId = context["dag_run"].conf["taskId"]
# #     key = f"{taskId}/{str(uuid.uuid4())}.mp4"
# #     s3.load_file_obj(outfile, key, "edenartlab-dev")
    
# #     return {
# #         "output": f"https://edenartlab-dev.s3.amazonaws.com/{key}",
# #         "thumbnail": image
# #     }





class MonologueRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview" 
    params: dict = {}

class TTSRequest(BaseModel):
    prompt: str
    voice: str

@router.post("/dags/monologue")
async def monologue_dag(request: MonologueRequest):
    #result = await monologue(request)
    result = {
        "prompt": "lucy is a dog",
        "voice": "Adam"
    }
    print(result)

    prompt = result["prompt"]
    voice = result["voice"]
    
    audio = elevenlabs.generate(prompt, voice=voice)
    audio_url = s3.upload(audio, "test.mp3")
    # audio_url = "https://edenartlab-dev.s3.amazonaws.com/test.mp3"
    print(audio_url)

    image = "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/e79da30c574bb31ede5eb7c04a9b91517ccc8cf0a3e29d4088bdcca9d4ef777b.jpg"
    config = {
        "face_url": image,
        "speech_url": audio_url,
        "gfpgan": False,
        "gfpgan_upscale": 1
    }

    
    # output = run_replicate_task(w2l_config, model_name=CHARACTER_GENERATOR)

    #     out_list = list(output)
    #     outfile_url = out_list[0]["files"][0]
    print(replicate)
    print(replicate.run_task)
    print("GO 2!")
    output = replicate.wav2lip(config)
    print(output)

    
    
    
    output_url = s3.upload(output, "test.mp4")
    print(output_url)



class DialogueRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview" 
    params: dict = {}

@router.post("/dags/dialogue")
async def dialogue_dag(request: DialogueRequest):
   print("DIA")
   print(request)