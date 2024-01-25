import os
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

NARRATOR_CHARACTER_ID = os.getenv("NARRATOR_CHARACTER_ID")


class TaskRequest(BaseModel):
    generatorName: str
    config: dict = {}
    webhookUrl: Optional[str] = None


class TaskResult(BaseModel):
    files: List[str] = []
    thumbnails: List[str] = []
    name: str = ""
    attributes: dict = {}
    progress: int = 0
    isFinal: bool = False


class TaskUpdate(BaseModel):
    id: str
    status: str
    output: TaskResult
    error: Optional[str] = None


class MonologueRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class MonologueResult(BaseModel):
    monologue: str


class DialogueRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class DialogueResult(BaseModel):
    dialogue: List[dict]


class StoryRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    narrator_id: str = NARRATOR_CHARACTER_ID
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class StoryVoiceoverMode(Enum):
    character = "character"
    narrator = "narrator"
    # none = 'none'


class StoryClip(BaseModel):
    """
    A single clip in a screenplay sequence
    """

    voiceover: StoryVoiceoverMode = Field(description="Voiceover mode for clip")
    character: Optional[str] = Field(
        description="Character name if voiceover mode is character, otherwise null"
    )
    speech: str = Field(description="Spoken text for clip")
    image_description: str = Field(description="Image content for clip")


class ComicRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class ComicPanel(BaseModel):
    """
    A single panel in a comic book sequence
    """

    image: str = Field(description="Literal description of image content for panel")
    caption: str = Field(description="Creative caption of panel")


class ComicResult(BaseModel):
    """
    A screenplay consisting of a sequence of clips
    """

    panels: List[ComicPanel] = Field(description="Comic Book panels")


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


class SummaryRequest(BaseModel):
    text: str
    model: str = "gpt-4-1106-preview"


class SummaryResult(BaseModel):
    summary: str


class ModerationRequest(BaseModel):
    text: str
    model: str = "gpt-3.5-turbo"


class ModerationResult(BaseModel):
    """
    Moderation scores for each category
    """

    nsfw: int = Field(description="Sexually explicit or nudity")
    gore: int = Field(description="Violence or gore")
    hate: int = Field(description="Hate, abusive or toxic speech")
    spam: int = Field(description="Spam, scam, or deceptive content")
