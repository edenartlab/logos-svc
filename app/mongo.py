import os
import pymongo
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
from dotenv import load_dotenv

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def search_character(name: str):
    character = db["characters"].find_one(
        {"$text": {"$search": name}, "logosData": {"$exists": True}},
        sort=[("createdAt", DESCENDING)],
    )

    if character:
        return character
    else:
        print(f"No character found with name: {name}")
        return None


def get_character_data(character_id: str):

    character = db["characters"].find_one({"_id": ObjectId(character_id)})

    if not character:
        print(f"---Character not found: {character_id}")
        raise Exception("Character not found")

    return character
