from typing import Optional, List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from ..mongo import get_character_data
from ..llm import LLM
from ..utils import clean_text
from ..prompt_templates.cinema import (
    screenwriter_template, 
    director_template, 
    cinematographer_template
)
router = APIRouter()


class StoryRequest(BaseModel):
    prompt: str
    model: str = "gpt-4-1106-preview" 
    params: dict = {}

@router.post("/story")
async def story(request: StoryRequest):
    try:
        params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

        screenwriter_message = str(screenwriter_template)    
        director_message = str(director_template)
        cinematographer_message = str(cinematographer_template)

        screenwriter = LLM(model=request.model, system_message=screenwriter_message, params=params, id="storyteller")
        director = LLM(model=request.model, system_message=director_message, params=params, id="director")
        cinematographer = LLM(model=request.model, system_message=cinematographer_message, params=params, id="cinematographer")

        story = screenwriter(request.prompt)
        stills = director(story)
        design = cinematographer(stills)

        stills = stills.split("\n")
        stills = [clean_text(still) for still in stills]

        print("GI")
        print(stills)
        return stills

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
