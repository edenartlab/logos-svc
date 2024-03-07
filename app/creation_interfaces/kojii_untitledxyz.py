import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class Type(Enum):
    column = "column"
    context = "context"

class KojiiUntitledxyzRequest(BaseModel):
    """
    A request for Untitledxyz endpoint
    """
    type: Type = Field(default=Type.column, description="Column or Context")
    human_machine_nature: float = Field(default=0.5, description="Human (0) vs machine (0.5) vs nature (1)", ge=0.0, le=1.0)

def kojii_untitledxyz(request: KojiiUntitledxyzRequest, callback=None):
    return {"hello": "world"}