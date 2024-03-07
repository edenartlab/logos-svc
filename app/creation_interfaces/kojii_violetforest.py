import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class Style(Enum):
    Kawaii = "Kawaii"
    Stars = "Stars"
    Lace = "Lace"
    Flowers = "Flowers"

class KojiiVioletforestRequest(BaseModel):
    """
    A request for VioletForest endpoint
    """
    cybertwee_cyberpunk: float = Field(default=0.5, description="Cybertwee vs Cyberpunk", ge=0.0, le=1.0)
    style: Style = Field(default=Style.Kawaii, description="Style")


def kojii_violetforest(request: KojiiVioletforestRequest, callback=None):
    if request.style == Style.Kawaii:
        modifiers = "kawaii, kawaii, kawaii, kawaii"
    elif request.style == Style.Stars:
        modifiers = "stars, stars, stars, stars"
    elif request.style == Style.Lace:
        modifiers = "lace, lace, lace, lace"
    elif request.style == Style.Flowers:
        modifiers = "flowers, flowers, flowers, flowers"
        
    prompt1 = f"a stunning image of a cute cybertwee girl, {modifiers}"
    prompt2 = f"a stunning image of an Aston Martin sportscar, {modifiers}"

    config = {
        "mode": "create",
        "text_input": prompt1,
        "lora": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/e3b036c0a9949de0a5433cb6c7e54b540c47535ce7ae252948177304542ca4da.tar",
        "lora_scale": 0.7,
    }

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url