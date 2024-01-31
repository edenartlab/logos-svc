import os
import uuid
import requests
from fastapi import BackgroundTasks

from .animations import (
    animated_monologue, 
    animated_dialogue, 
    animated_story, 
    illustrated_comic,
    little_martian_poster
)
from .models import MonologueRequest, MonologueResult
from .models import DialogueRequest, DialogueResult, StoryRequest
from .models import TaskRequest, TaskUpdate, TaskResult, LittleMartianRequest

NARRATOR_CHARACTER_ID = os.getenv("NARRATOR_CHARACTER_ID")


def process_task(task_id: str, request: TaskRequest):
    print("config", request.config)

    task_type = request.generatorName
    webhook_url = request.webhookUrl
    
    update = TaskUpdate(
        id=task_id,
        output=TaskResult(progress=0),
        status="processing",
        error=None,
    )

    if webhook_url:
        requests.post(webhook_url, json=update.dict())

    try:
        if task_type == "monologue":
            character_id = request.config.get("characterId")
            prompt = request.config.get("prompt")
            task_req = MonologueRequest(
                character_id=character_id,
                prompt=prompt,
            )
            output_url, thumbnail_url = animated_monologue(task_req)

        elif task_type == "dialogue":
            character_ids = request.config.get("characterIds")
            prompt = request.config.get("prompt")
            task_req = DialogueRequest(
                character_ids=character_ids,
                prompt=prompt,
            )
            output_url, thumbnail_url = animated_dialogue(task_req)

        elif task_type == "story":
            character_ids = request.config.get("characterIds")
            prompt = request.config.get("prompt")
            task_req = StoryRequest(
                character_ids=character_ids,
                prompt=prompt,
                narrator_id=NARRATOR_CHARACTER_ID,
            )
            output_url, thumbnail_url = animated_story(task_req)

        elif task_type == "comic":
            character_id = request.config.get("characterId")
            prompt = request.config.get("prompt")
            task_req = ComicRequest(
                character_id=character_id,
                prompt=prompt,
            )
            output_url, thumbnail_url = illustrated_comic(task_req)

        elif task_type == "littlemartians":
            martian = request.config.get("martian")
            prompt = request.config.get("prompt")
            setting = request.config.get("setting")
            genre = request.config.get("genre")
            aspect_ratio = request.config.get("aspect_ratio")
            task_req = LittleMartianRequest(
                martian=martian,
                prompt=prompt,
                setting=setting,
                genre=genre,
                aspect_ratio=aspect_ratio,
            )
            output_url, thumbnail_url = little_martian_poster(task_req)

        output = TaskResult(
            files=[output_url],
            thumbnails=[thumbnail_url],
            name=prompt,
            attributes={},
            progress=1,
            isFinal=True,
        )
        status = "succeeded"
        error = None

    except Exception as e:
        output = TaskResult(
            files=[],
            thumbnails=[],
            name=prompt,
            attributes={},
            progress=0,
            isFinal=True,
        )
        status = "failed"
        error = str(e)

    update = TaskUpdate(
        id=task_id,
        output=output,
        status=status,
        error=error,
    )
    print("update", update.dict())

    if webhook_url:
        requests.post(webhook_url, json=update.dict())


async def generate_task(background_tasks: BackgroundTasks, request: TaskRequest):
    task_id = str(uuid.uuid4())
    print("MAKE A TASK!!")
    if request.generatorName in ["monologue", "dialogue", "story", "littlemartians"]:
        background_tasks.add_task(process_task, task_id, request)
    return {"id": task_id}
