from enum import Enum
from typing import Optional, List, Any
from pydantic import BaseModel, Field


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


class SummaryRequest(BaseModel):
    text: str
    model: str = "gpt-4-1106-preview"
    params: dict = {}


class ModerationRequest(BaseModel):
    text: str
    model: str = "gpt-3.5-turbo"
    params: dict = {}


class SimpleAssistantRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    params: dict = {}
    output_schema: Any = None


class ModerationResult(BaseModel):
    """
    Moderation scores for each category
    """

    nsfw: int = Field(description="Sexually explicit or nudity")
    gore: int = Field(description="Violence or gore")
    hate: int = Field(description="Hate, abusive or toxic speech")
    spam: int = Field(description="Spam, scam, or deceptive content")
