from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel

from ..mongo import get_character_data
from ..llm import LLM
from ..utils import text_to_lines
from ..prompt_templates.cinema import (
    screenwriter_template,
    director_template,
    cinematographer_template,
)

router = APIRouter()


class CinemaRequest(BaseModel):
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}

class CinemaResult(BaseModel):
    stills: List[str]

@router.post("/story/cinema")
async def cinema(request: CinemaRequest):
    params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

    screenwriter_message = str(screenwriter_template)
    director_message = str(director_template)
    cinematographer_message = str(cinematographer_template)

    screenwriter = LLM(
        model=request.model,
        system_message=screenwriter_message,
        params=params,
    )
    director = LLM(
        model=request.model,
        system_message=director_message,
        params=params,
    )
    cinematographer = LLM(
        model=request.model,
        system_message=cinematographer_message,
        params=params,
    )

    story = screenwriter(request.prompt)
    stills = director(story)
    design = cinematographer(stills)

    stills = text_to_lines(stills) 
    
    result = CinemaResult(stills=stills)

    return result


class ComicRequest(BaseModel):
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}

class ComicResult(BaseModel):
    comic: List[str]

@router.post("/story/comic")
async def comic(request: ComicRequest):
    print("TBD comic")
    result = ComicResult(comic=["TBD"])
    return result
