from typing import Optional, List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from ..mongo import get_character_data
from ..llm import LLM
from ..prompt_templates import monologue_template, dialogue_template

router = APIRouter()


class MonologueRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview" 
    params: dict = {}

@router.post("/scenarios/monologue")
async def monologue(request: MonologueRequest):
    try:
        params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

        character_data = get_character_data(request.character_id)
        name = character_data.get("name")
        description = character_data.get("logosData").get("identity")

        system_message = monologue_template.substitute(
            name=name,
            description=description
        )
        
        llm = LLM(model=request.model, system_message=system_message, params=params)
        message = llm(request.prompt)
        
        result = {"message": message}

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class DialogueRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview" 
    params: dict = {}

@router.post("/scenarios/dialogue")
async def dialogue(request: DialogueRequest):
    try:
        params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

        characters = [get_character_data(character_id) for character_id in request.character_ids]
        
        llms = []       
        for c, character in enumerate(characters):
            other_character = characters[(c+1)%2]
            system_message = dialogue_template.substitute(
                name=character.get("name"),
                description=character.get("logosData").get("identity"),
                other_name=other_character.get("name"),
                other_description=other_character.get("logosData").get("identity"),
                prompt=request.prompt
            )
            llms.append(LLM(model=request.model, system_message=system_message, params=params))

        message = "You are beginning the conversation. What is the first thing you say? Just the line. No quotes, no name markers."

        print("GO!!!!")

        conversation = []

        for m in range(4):
            llm = llms[m % 2]
            message = llm(message)

            if not message:
                raise Exception("No response from character")

            conversation.append({"character": request.character_ids[m%2], "message": message})

        result = {"conversation": conversation}
        print(result)

        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
