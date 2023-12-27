from fastapi import APIRouter, Body, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field

from ..character import Character

router = APIRouter()

characters = {}

class ChatRequest(BaseModel):
    character_id: str
    session_id: str
    prompt: str
    attachments: Optional[List[str]] = Field(None)

@router.post("/scenarios/chat")
async def chat(request: ChatRequest):
    try:
        character_id = request.character_id        
        if character_id not in characters:
            characters[character_id] = Character(character_id)
        
        character = characters[character_id]
        character.update()

        message = {
            "prompt": request.prompt,
            "attachments": request.attachments,
        }

        response = character(message, session_id=request.session_id)

        return response

    except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))









# import logging
# import os
# from typing import Optional, List
# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from pydantic import BaseModel, Field
# import pymongo
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from dotenv import load_dotenv

# print("yo")
# import scenarios

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# app = FastAPI()
# client = MongoClient(MONGO_URI)
# db = client[MONGO_DB_NAME]
# characters = {}


# def get_character_data(character_id: str):
#     character = db["characters"].find_one({"_id": ObjectId(character_id)})
    
#     print("CHAR DATA", character)

#     if not character:
#         raise Exception("Character not found")
    
#     logos_data = character.get("logosData")
    
#     name = character.get("name")
#     identity = logos_data.get("identity")
#     knowledge = logos_data.get("knowledge")
#     knowledge_summary = logos_data.get("knowledgeSummary")
#     concept = logos_data.get("concept")

#     smart_reply = False
    
#     return (name, identity, knowledge_summary, knowledge, True, concept), smart_reply








# import logging
# import os
# from typing import Optional, List
# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from pydantic import BaseModel, Field
# import pymongo
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from dotenv import load_dotenv

# print("yo")
# import scenarios
# from .scenarios.eden_assistant import EdenAssistant

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# app = FastAPI()
# client = MongoClient(MONGO_URI)
# db = client[MONGO_DB_NAME]
# characters = {}


# def get_character_data(character_id: str):
#     character = db["characters"].find_one({"_id": ObjectId(character_id)})
    
#     print("CHAR DATA", character)

#     if not character:
#         raise Exception("Character not found")
    
#     logos_data = character.get("logosData")
    
#     name = character.get("name")
#     identity = logos_data.get("identity")
#     knowledge = logos_data.get("knowledge")
#     knowledge_summary = logos_data.get("knowledgeSummary")
#     concept = logos_data.get("concept")

#     smart_reply = False
    
#     return (name, identity, knowledge_summary, knowledge, True, concept), smart_reply


# class ThinkingInput(BaseModel):
#     character_id: str
#     session_id: str
#     prompt: str

# @app.post("/think")
# async def think(interaction: ThinkingInput):

#     if interaction.character_id not in characters:
#         characters[interaction.character_id] = EdenAssistant()

#     character = characters[interaction.character_id]

#     character_data, smart_reply = get_character_data(interaction.character_id)
#     character.update(*character_data)

#     if not smart_reply:
#         return False

#     reply = character.smart_reply(interaction.prompt)
#     result = {"reply": reply}

#     return result
    

# class InteractionInput(BaseModel):
#     character_id: str
#     session_id: str
#     prompt: str
#     attachments: Optional[List[str]] = Field(None)

# @app.post("/interact")
# async def interact(interaction: InteractionInput):
    
#     if interaction.character_id not in characters:
#         characters[interaction.character_id] = EdenAssistant()

#     character = characters[interaction.character_id]
    
#     character_data, _ = get_character_data(interaction.character_id)
#     character.update(*character_data)

#     message = {
#         "prompt": interaction.prompt,
#         "attachments": interaction.attachments,
#     }

#     response = character(message, session_id=interaction.session_id)

#     return response
