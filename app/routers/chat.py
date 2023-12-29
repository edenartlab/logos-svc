from fastapi import APIRouter, Body, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field

from ..character import Character, EdenCharacter

router = APIRouter()

characters = {}


def get_character(character_id: str):
    if character_id not in characters:
        characters[character_id] = EdenCharacter(character_id)
    character = characters[character_id]
    return character


class ChatTestRequest(BaseModel):
    name: str
    identity: str
    knowledge_summary: Optional[str] = Field(None)
    knowledge: Optional[str] = Field(None)
    prompt: str
    attachments: Optional[List[str]] = Field(None)


@router.post("/chat/test")
async def test(request: ChatTestRequest):
    character = Character(
        name=request.name,
        identity=request.identity,
        knowledge_summary=request.knowledge_summary,
        knowledge=request.knowledge,
        creation_enabled=False,
        concept=None,
        smart_reply=False,
    )
    message = {
        "prompt": request.prompt,
        "attachments": request.attachments,
    }
    response = character(message, session_id="test")
    return response


class ChatRequest(BaseModel):
    character_id: str
    session_id: str
    prompt: str
    attachments: Optional[List[str]] = Field(None)


@router.post("/chat/think")
async def think(request: ChatRequest):
    character = get_character(request.character_id)
    character.sync()
    message = {
        "prompt": request.prompt,
        "attachments": request.attachments,
    }
    response = character.think(message)
    return response


@router.post("/chat/speak")
async def speak(request: ChatRequest):
    character = get_character(request.character_id)
    message = {
        "prompt": request.prompt,
        "attachments": request.attachments,
    }
    response = character(message, session_id=request.session_id)
    return response
