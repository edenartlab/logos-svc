import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..utils import now_tz


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
