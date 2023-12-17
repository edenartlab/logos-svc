from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from logos.scenarios.eden_assistant import EdenAssistant
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class EdenAssistantInput(BaseModel):
    name: str
    identity: str
    knowledge_summary: str
    knowledge: str


class InteractionInput(BaseModel):
    prompt: str
    author_id: str
    attachments: Optional[list]


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
