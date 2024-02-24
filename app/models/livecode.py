from typing import Optional, List
from pydantic import BaseModel, Field


class LiveCodeRequest(BaseModel):
    """
    A chat request to a LiveCoder
    """

    session_id: str
    message: str


class LiveCodeResult(BaseModel):
    """
    A result from a LiveCoder
    """

    message: str
    code: str