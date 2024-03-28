from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


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
    seed: Optional[int] = Field(default=None, description="Random seed")
