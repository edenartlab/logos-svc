import logging
import os
from typing import List, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

from .scenarios.eden_assistant import EdenAssistant

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

app = FastAPI()
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
characters = {}


def get_character_data(character_id: str):
    character = db["characters"].find_one({"_id": ObjectId(character_id)})

    if not character:
        raise Exception("Character not found")

    logos_data = character.get("logosData")

    name = character.get("name")
    identity = logos_data.get("identity")
    knowledge = logos_data.get("knowledge")
    knowledge_summary = logos_data.get("knowledgeSummary")

    return name, identity, knowledge, knowledge_summary


class EdenAssistantInput(BaseModel):
    name: str
    identity: str
    knowledge_summary: Optional[str] = Field(None)
    knowledge: Optional[str] = Field(None)


class InteractionInput(BaseModel):
    prompt: str
    author_id: str
    attachments: Optional[List[str]] = Field(None)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.post("/interact")
async def interact(assistant: EdenAssistantInput, interaction: InteractionInput):
    if interaction.character_id not in characters:
        characters[interaction.character_id] = EdenAssistant()

    character = characters[interaction.character_id]
    character_data = get_character_data(interaction.character_id)
    print(character_data)
    character.update(*character_data)
    message = {
        "prompt": interaction.prompt,
        "attachments": interaction.attachments,
    }

    response = character(message, session_id=interaction.session_id)
    print(response)

    return response


@app.post("/test")
async def test(assistant: EdenAssistantInput, interaction: InteractionInput):
    character = EdenAssistant(
        name=assistant.name,
        identity=assistant.identity,
        knowledge=assistant.knowledge,
        knowledge_summary=assistant.knowledge_summary,
    )
    message = {
        "prompt": interaction.prompt,
        "attachments": interaction.attachments,
    }
    response = character(message, session_id=interaction.author_id)
    print(response)
    return response
