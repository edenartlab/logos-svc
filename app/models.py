import os
import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from .utils import now_tz

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
    num_clips: int = 5
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


class Poster(BaseModel):
    """
    A single panel or poster in a comic book sequence or other
    """

    image: str = Field(description="Literal description of image content for [poster or panel]")
    caption: str = Field(description="Creative caption of poster or panel")


class ComicResult(BaseModel):
    """
    A screenplay consisting of a sequence of clips
    """

    panels: List[Poster] = Field(description="Comic Book panels")


class Martian(Enum):
    Verdelis = "Verdelis"
    Shuijing = "Shuijing"
    Kweku = "Kweku"
    Ada = "Ada"
    Kalama = "Kalama"
    Mycos = "Mycos"

class Setting(Enum):
    physical_reality = "Physical Reality"
    imaginarium = "Human Imaginarium"

class Genre(Enum):
    drama = "Drama"
    comedy = "Comedy"
    horror = "Horror"
    mystery = "Mystery"
    action = "Action"

class AspectRatio(Enum):
    portrait = "portrait"
    landscape = "landscape"
    square = "square"

class LittleMartianRequest(BaseModel):
    """
    A request for Little Martians poster
    """

    martian: Martian
    prompt: str
    setting: Setting
    genre: Genre
    aspect_ratio: AspectRatio
    model: str = "gpt-4-1106-preview"
    params: dict = {}


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


class ChatMessage(BaseModel):
    """
    A single chat message
    """

    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[str] = None
    received_at: datetime.datetime = Field(default_factory=now_tz)
    finish_reason: Optional[str] = None
    prompt_length: Optional[int] = None
    completion_length: Optional[int] = None
    total_length: Optional[int] = None

    def __str__(self) -> str:
        return str(
            self.model_dump(
                exclude_none=True,
                # option=orjson.OPT_INDENT_2
            )
        )
