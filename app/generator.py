import os
import uuid
import requests
from fastapi import BackgroundTasks

from .models import (
    MonologueRequest,
    DialogueRequest, DialogueResult, StoryRequest,
    TaskRequest, TaskUpdate, TaskResult, LittleMartianRequest
)
from .animations import (
    animated_monologue, 
    animated_dialogue, 
    animated_story, 
    illustrated_comic,
    little_martian_poster
)

NARRATOR_CHARACTER_ID = os.getenv("NARRATOR_CHARACTER_ID")


def process_task(task_id: str, request: TaskRequest):
    print("config", request.config)

    task_type = request.generatorName
    webhook_url = request.webhookUrl

    def send_progress_update(progress: float):
        if webhook_url:
            update = TaskUpdate(
                id=task_id,
                output=TaskResult(progress=progress),
                status="processing",
                error=None,
            )
            requests.post(webhook_url, json=update.dict())
    

    if webhook_url:
        update = TaskUpdate(
            id=task_id,
            output=TaskResult(progress=0),
            status="processing",
            error=None,
        )
        requests.post(webhook_url, json=update.dict())

    try:
        if task_type == "monologue":
            character_id = request.config.get("characterId")
            prompt = request.config.get("prompt")
            gfpgan = request.config.get("gfpgan")
            dual_view = request.config.get("dual_view")
            task_req = MonologueRequest(
                character_id=character_id,
                prompt=prompt,
                gfpgan=gfpgan,
                dual_view=dual_view,
            )
            output_url, thumbnail_url = animated_monologue(
                task_req,
                callback=send_progress_update
            )

        elif task_type == "dialogue":
            character_ids = request.config.get("characterIds")
            prompt = request.config.get("prompt")
            gfpgan = request.config.get("gfpgan")
            dual_view = request.config.get("dual_view")
            intro_screen = request.config.get("intro_screen")
            task_req = DialogueRequest(
                character_ids=character_ids,
                prompt=prompt,
                gfpgan=gfpgan,
                dual_view=dual_view,
                intro_screen=intro_screen
            )
            output_url, thumbnail_url = animated_dialogue(
                task_req,
                callback=send_progress_update
            )

        elif task_type == "story":
            character_ids = request.config.get("characterIds")
            prompt = request.config.intro_screenget("prompt")
            intro_screen = request.config.get("intro_screen")
            task_req = StoryRequest(
                character_ids=character_ids,
                prompt=prompt,
                narrator_id=NARRATOR_CHARACTER_ID,
                intro_screen=intro_screen,
            )
            output_url, thumbnail_url = animated_story(
                task_req,
                callback=send_progress_update
            )

        elif task_type == "comic":
            character_id = request.config.get("characterId")
            prompt = request.config.get("prompt")
            task_req = ComicRequest(
                character_id=character_id,
                prompt=prompt,
            )
            output_url, thumbnail_url = illustrated_comic(
                task_req,
                callback=send_progress_update
            )

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
            output_url, thumbnail_url = little_martian_poster(
                task_req,
                callback=send_progress_update
            )

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

    if webhook_url:
        update = TaskUpdate(
            id=task_id,
            output=output,
            status=status,
            error=error,
        )
        print("update", update.dict())
        requests.post(webhook_url, json=update.dict())


async def generate_task(background_tasks: BackgroundTasks, request: TaskRequest):
    task_id = str(uuid.uuid4())
    if request.generatorName in ["monologue", "dialogue", "story", "littlemartians"]:
        background_tasks.add_task(process_task, task_id, request)
    return {"id": task_id}
