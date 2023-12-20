import logging
import os
from typing import Optional, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

from .scenarios.eden_assistant import EdenAssistant

load_dotenv()

print("SECRETS")
print(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
print("SECRETS")
print(MONGO_URI, MONGO_DB_NAME)
print("SECRETS")

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
    character_id: str
    session_id: str
    prompt: str
    attachments: Optional[List[str]] = Field(None)


@app.post("/interact")
async def interact(assistant: EdenAssistantInput, interaction: InteractionInput):

    print("INTERACTON REQUEST")
    print(assistant)
    print(interaction)
    print("------")
    if interaction.character_id not in characters:
        characters[interaction.character_id] = EdenAssistant()

    character = characters[interaction.character_id]
    character_data = get_character_data(interaction.character_id)
    character.update(*character_data)

    message = {
        "prompt": interaction.prompt,
        "attachments": interaction.attachments,
    }

    response = character(message, session_id=interaction.session_id)
    print(response)

    return response

