import os
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..utils import now_tz

NARRATOR_CHARACTER_ID = os.getenv("NARRATOR_CHARACTER_ID")


class MonologueRequest(BaseModel):
    character_id: str
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}
    gfpgan: bool = False
    intro_screen: bool = False


class MonologueResult(BaseModel):
    monologue: str


class DialogueRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}
    gfpgan: bool = False
    intro_screen: bool = False
    dual_view: bool = False


class DialogueResult(BaseModel):
    dialogue: List[dict]


class StoryRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    narrator_id: str = NARRATOR_CHARACTER_ID
    num_clips: int = 5
    model: str = "gpt-4-1106-preview"
    params: dict = {}
    intro_screen: bool = False


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


class StoryResult(BaseModel):
    """
    A screenplay consisting of a sequence of clips
    """
    clips: List[StoryClip] = Field(description="Clips in the sequence")


class ReelRequest(BaseModel):
    character_ids: List[str]
    prompt: str
    narrator_id: str = NARRATOR_CHARACTER_ID
    model: str = "gpt-4-1106-preview"
    params: dict = {}
    intro_screen: bool = False


class ReelVoiceoverMode(Enum):
    character = "character"
    narrator = "narrator"
    none = "none"


class ReelResult(BaseModel):
    """
    A screenplay consisting of a sequence of clips
    """
    voiceover: ReelVoiceoverMode = Field(description="Voiceover mode for reel")
    character: Optional[str] = Field(
        description="Character name if voiceover mode is character, otherwise null"
    )
    speech: Optional[str] = Field(description="Spoken text for clip if voiceover mode is not none, otherwise null")
    music_description: str = Field(description="Music content for reel")
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

