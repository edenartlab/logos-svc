from typing import List, Optional
from pydantic import BaseModel, Field
from logos.scenarios.eden_assistant import EdenAssistant
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

load_dotenv()

app = FastAPI()


class EdenAssistantInput(BaseModel):
    name: str
    identity: str
    knowledge_summary: Optional[str] = Field(None)
    knowledge: Optional[str] = Field(None)


class InteractionInput(BaseModel):
    prompt: str
    author_id: str
    attachments: Optional[List[str]] = Field(None)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.post("/interact")
async def interact(assistant: EdenAssistantInput, interaction: InteractionInput):
    assistant_message = {
        "prompt": interaction.prompt,
        "attachments": interaction.attachments,
    }

    # Initialize EdenAssistant
    assistant = EdenAssistant(
        name=assistant.name,
        identity=assistant.identity,
        knowledge_summary=assistant.knowledge_summary,
        knowledge=assistant.knowledge,
    )

    # Do a completion with the context
    response = assistant(assistant_message, session_id=interaction.author_id)
    print(response)

    return response
