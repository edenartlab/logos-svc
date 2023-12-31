from typing import Optional, List
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import traceback
import logging
import time
import requests

from .dags import monologue_dag, dialogue_dag
from ..mongo import get_character_data
from ..llm import LLM
from ..prompt_templates import monologue_template, dialogue_template

from ..models import MonologueRequest, MonologueOutput
from ..models import DialogueRequest, DialogueOutput
from ..models import TaskRequest, TaskUpdate, TaskOutput

router = APIRouter()

def process_task(task_id: str, request: TaskRequest, task_type: str):
    webhook_url = request.webhookUrl 
    print("config", request.config)
    
    prompt = request.config.get("prompt")

    try:
        if task_type == "monologue":
            character_id = request.config.get("characterId")
            task_req = MonologueRequest(
                character_id=character_id,
                prompt=prompt,
            )
            output_url, thumbnail_url = monologue_dag(task_req)
        
        elif task_type == "dialogue":
            character_ids = request.config.get("characterIds")
            task_req = DialogueRequest(
                character_ids=character_ids,
                prompt=prompt,
            )
            output_url, thumbnail_url = dialogue_dag(task_req)
        
        output = TaskOutput(
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
        output = TaskOutput(
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

    requests.post(webhook_url, json=update.dict())


@router.post("/tasks/create")
async def generate_task(background_tasks: BackgroundTasks, request: TaskRequest):
    task_id = str(uuid.uuid4())
    if request.generatorName in ["monologue", "dialogue"]:
        background_tasks.add_task(process_task, task_id, request, request.generatorName)
    return {"id": task_id}