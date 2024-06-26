import re
import os
import uuid
import requests
from fastapi import BackgroundTasks

from .scenarios.tasks import general_assistant
from .models.tasks import SimpleAssistantRequest

from .models import (
    MonologueRequest,
    DialogueRequest,
    DialogueResult,
    StoryRequest,
    ReelRequest,
    TaskRequest,
    TaskUpdate,
    TaskResult,
    LittleMartianRequest,
)
from .animations import (
    animated_monologue,
    animated_dialogue,
    animated_story,
    animated_reel,
    illustrated_comic,
    little_martian_poster,
)
from .creation_interfaces import (
    kojii_makeitrad,
    KojiiMakeitradRequest,
    kojii_chebel,
    KojiiChebelRequest,
    kojii_untitledxyz,
    KojiiUntitledxyzRequest,
    kojii_violetforest,
    KojiiVioletforestRequest,
    kojii_huemin,
    KojiiHueminRequest,
)

NARRATOR_CHARACTER_ID = os.getenv("NARRATOR_CHARACTER_ID")

logosGenerators = [
    "monologue",
    "dialogue",
    "story",
    "reel",
    "kojii/makeitrad",
    "kojii/va2rosa",
    "kojii/chebel",
    "kojii/untitledxyz",
    "kojii/violetforest",
    "kojii/huemin",
]


def name_interaction(prompt: str):
    naming_prompt = f"Take the following text prompt and output a short phrase or sentence with 5-15 words which captures the essence of the text. It will be used to give a name to the interaction. If the text given is already a short phrase, just output that. Output *only* the short phrase. Do not include pretext, restatement, or other extraneous text.\n\n---\n\nText:\n {prompt}"
    print("----")
    print(naming_prompt)
    request = SimpleAssistantRequest(
        prompt=naming_prompt,
        model="gpt-3.5-turbo",
        params={"temperature": 0.0, "max_tokens": 100},
    )
    try:
        name = general_assistant(request)
    except Exception as e:
        name = re.sub(r"\W+", " ", prompt).replace("\n", "").replace("\r", "")[:100]
    print(name)
    print("----")
    return name


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
            init_image = request.config.get("init_image")
            gfpgan = request.config.get("gfpgan")
            task_req = MonologueRequest(
                character_id=character_id,
                prompt=prompt,
                init_image=init_image,
                gfpgan=gfpgan,
            )
            output_url, thumbnail_url = animated_monologue(
                task_req,
                callback=send_progress_update,
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
                intro_screen=intro_screen,
            )
            output_url, thumbnail_url = animated_dialogue(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "story":
            character_ids = request.config.get("characterIds")
            prompt = request.config.get("prompt")
            intro_screen = request.config.get("intro_screen")
            music_prompt = request.config.get("music_prompt")
            music = request.config.get("music")
            task_req = StoryRequest(
                character_ids=character_ids,
                prompt=prompt,
                narrator_id=NARRATOR_CHARACTER_ID,
                music_prompt=music_prompt,
                music=music,
                intro_screen=intro_screen,
            )
            output_url, thumbnail_url = animated_story(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "reel":
            character_ids = request.config.get("characterIds")
            prompt = request.config.get("prompt")
            intro_screen = request.config.get("intro_screen")
            narration = request.config.get("narration")
            music_prompt = request.config.get("music_prompt")
            aspect_ratio = request.config.get("aspect_ratio")
            task_req = ReelRequest(
                character_ids=character_ids,
                prompt=prompt,
                music_prompt=music_prompt,
                aspect_ratio=aspect_ratio,
                narration=narration,
                narrator_id=NARRATOR_CHARACTER_ID,
                intro_screen=intro_screen,
            )
            output_url, thumbnail_url = animated_reel(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "kojii/makeitrad":
            setting = request.config.get("setting")
            location = request.config.get("location")
            time = request.config.get("time")
            color = request.config.get("color")
            clouds = request.config.get("clouds")
            pool = request.config.get("pool")
            aspect_ratio = request.config.get("aspect_ratio")
            prompt = (
                f"{setting} {location} {time} {color} {clouds} {pool} {aspect_ratio}"
            )
            task_req = KojiiMakeitradRequest(
                setting=setting,
                location=location,
                time=time,
                color=color,
                clouds=clouds,
                pool=pool,
                aspect_ratio=aspect_ratio,
            )
            output_url, thumbnail_url = kojii_makeitrad(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "kojii/va2rosa":
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
                callback=send_progress_update,
            )

        elif task_type == "kojii/chebel":
            number = request.config.get("number")
            aspect_ratio = request.config.get("aspect_ratio")
            abstract = request.config.get("abstract")
            color = request.config.get("color")
            prompt = f"{number} {aspect_ratio} {abstract} {color}"
            task_req = KojiiChebelRequest(
                number=number,
                aspect_ratio=aspect_ratio,
                abstract=abstract,
                color=color,
            )
            output_url, thumbnail_url = kojii_chebel(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "kojii/untitledxyz":
            type = request.config.get("type")
            human_machine_nature = request.config.get("human_machine_nature")
            prompt = f"{type} {human_machine_nature}"
            task_req = KojiiUntitledxyzRequest(
                type=type,
                human_machine_nature=human_machine_nature,
            )
            output_url, thumbnail_url = kojii_untitledxyz(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "kojii/violetforest":
            cybertwee_cyberpunk = request.config.get("cybertwee_cyberpunk")
            style = request.config.get("style")
            prompt = f"{cybertwee_cyberpunk} {style}"
            task_req = KojiiVioletforestRequest(
                cybertwee_cyberpunk=cybertwee_cyberpunk,
                style=style,
            )
            output_url, thumbnail_url = kojii_violetforest(
                task_req,
                callback=send_progress_update,
            )

        elif task_type == "kojii/huemin":
            climate = request.config.get("climate")
            landform = request.config.get("landform")
            body_of_water = request.config.get("body_of_water")
            prompt = f"{climate} {landform} {body_of_water}"
            task_req = KojiiHueminRequest(
                climate=climate,
                landform=landform,
                body_of_water=body_of_water,
            )
            output_url, thumbnail_url = kojii_huemin(
                task_req,
                callback=send_progress_update,
            )

        output = TaskResult(
            files=[output_url],
            thumbnails=[thumbnail_url],
            name=name_interaction(prompt),
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
            name="",
            attributes={},
            progress=0,
            isFinal=True,
        )
        status = "failed"
        error = str(e)
        print("error", error)

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
    if request.generatorName in logosGenerators:
        background_tasks.add_task(process_task, task_id, request)
    return {"id": task_id}
