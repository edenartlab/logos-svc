import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class KojiiHueminRequest(BaseModel):
    """
    A request for Huemin endpoint
    """
    prompt: Optional[str] = Field(default=None, description="Prompt")


def kojii_huemin(request: KojiiHueminRequest, callback=None):
    config = {
        "mode": "huemin",
        "prompt": request.prompt
    }

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url
