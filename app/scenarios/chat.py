from ..character import Character, EdenCharacter
from ..models import ChatRequest, ChatTestRequest, CharacterOutput

characters = {}

print("do chat")

def get_character(character_id: str):
    if character_id not in characters:
        characters[character_id] = EdenCharacter(character_id)
    character = characters[character_id]
    return character


def think(request: ChatRequest) -> bool:
    character = get_character(request.character_id)
    character.sync()
    message = {
        "message": request.message,
        "attachments": request.attachments,
    }
    response = character.think(message)
    return response


def speak(request: ChatRequest) -> CharacterOutput:
    character = get_character(request.character_id)
    message = {
        "message": request.message,
        "attachments": request.attachments,
    }
    response = character(message, session_id=request.session_id)
    return response


def test(request: ChatTestRequest):
    character = Character(
        name=request.name,
        identity=request.identity,
        knowledge_summary=request.knowledge_summary,
        knowledge=request.knowledge,
    )
    message = {
        "message": request.message,
        "attachments": request.attachments,
    }
    response = character(message, session_id="test")
    return response
