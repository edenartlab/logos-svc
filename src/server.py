import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

from .scenarios.eden_assistant import EdenAssistant

load_dotenv()

app = FastAPI()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]
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


class InteractionInput(BaseModel):
    character_id: str
    session_id: str
    prompt: str
    attachments: Optional[list]

@app.post("/interact")
async def interact(interaction: InteractionInput):

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
