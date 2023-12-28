import os
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def get_character_data(character_id: str):
    character = db["characters"].find_one({
        "_id": ObjectId(character_id)
    })

    if not character:
        raise Exception("Character not found")
    
    return character
