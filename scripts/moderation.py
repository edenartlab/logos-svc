import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

mongo = MongoClient(MONGO_URI)
db = mongo[MONGO_DB_NAME]


def iterate_collection(collection_name, callback, batch_size=100):
    docs = db[collection_name].find().batch_size(batch_size)
    try:        
        for doc in docs:
            callback(doc)
    finally:
        docs.close()


def moderation():

    def process_creation(creation):
        if 'task' not in creation:
            return        
        task = db["tasks"].find_one({
            "_id": ObjectId(creation['task'])
        })        
        if 'text_input' not in task['config']:
            return
        text_input = task['config']['text_input']
        print(text_input)
        request = {
            "text": text_input
        }
        response = client.post("/tasks/moderation", json=request)
        print(response.json())
        print("-----")


    iterate_collection(
        "creations", 
        process_creation
    )



moderation()