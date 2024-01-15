from typing import Optional, List
from pydantic import BaseModel, Field

from .character import Character


class TaskRequest(BaseModel):
    generatorName: str
    config: dict = {}
    webhookUrl: str


class TaskOutput(BaseModel):
    files: List[str] = []
    thumbnails: List[str] = []
    name: str = ""
    attributes: dict = {}
    progress: int = 0
    isFinal: bool = False


class TaskUpdate(BaseModel):
    id: str
    status: str
    output: TaskOutput
    error: Optional[str] = None


class MonologueRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class MonologueOutput(BaseModel):
    monologue: str


class DialogueRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class DialogueOutput(BaseModel):
    dialogue: List[dict]


class CinemaRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}

class CinemaResult(BaseModel):
    stills: List[str]


class ChatRequest(BaseModel):
    """
    A chat request to an EdenCharacter
    """

    character_id: str
    session_id: str
    message: str
    attachments: Optional[List[str]] = Field(None)


class ChatTestRequest(BaseModel):
    """
    A chat request to a Character
    """

    name: str
    identity: str
    knowledge_summary: Optional[str] = Field(None)
    knowledge: Optional[str] = Field(None)
    message: str
    attachments: Optional[List[str]] = Field(None)


class CharacterOutput(BaseModel):
    """
    Output of chat message from a Character
    """

    message: str = Field(description="Text response from Eden")
    config: Optional[dict] = Field(description="Config for Eden generator")


# class Character(BaseModel):
#     name: str
#     description: str
#     knowledge_summary: Optional[str] = None
#     knowledge: Optional[str] = None
#     voice: Optional[str] = None
#     image: Optional[str] = None


# export interface CharacterSchema extends VisibilitySchema {
#   user: UserDocument
#   name: string
#   slug: string
#   greeting?: string
#   dialogue?: ChatSchema[]
#   logosData?: LogosData
#   image?: string
#   voice?: string
#   creationCount?: number
#   createdAt?: Date
#   updatedAt?: Date
# }


class CharacterChatMessage(BaseModel):
    character: Character
    message: str

    def __str__(self):
        return f"{self.character.name}: {self.message}"
