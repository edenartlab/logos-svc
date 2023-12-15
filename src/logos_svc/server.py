from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from logos.scenarios.eden_assistant import EdenAssistant
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class EdenAssistantInput(BaseModel):
    character_description: str
    creator_prompt: str
    documentation_prompt: str
    documentation: str
    router_prompt: str


class InteractionInput(BaseModel):
    prompt: str
    author_id: str
    attachments: Optional[list]


@app.post("/interact")
async def interact(assistant: EdenAssistantInput, interaction: InteractionInput):
    attachment_lookup_file = {
        url: f"/files/image{i+1}.jpeg" for i, url in enumerate(interaction.attachments)
    }
    attachment_lookup_url = {v: k for k, v in attachment_lookup_file.items()}
    attachment_files = [attachment_lookup_file[url] for url in interaction.attachments]

    assistant_message = {
        "prompt": interaction.prompt,
        "attachments": attachment_files,
    }

    # Initialize EdenAssistant
    assistant = EdenAssistant(
        character_description=assistant.character_description,
        creator_prompt=assistant.creator_prompt,
        documentation_prompt=assistant.documentation_prompt,
        documentation=assistant.documentation,
        router_prompt=assistant.router_prompt,
    )

    # Do a completion with the context
    response = assistant(assistant_message, session_id=interaction.author_id)
    print(response)

    # replace the dummy URLs in response["config"] with the original URLs
    if response.get("config"):
        config = response["config"]
        if config.get("init_image"):
            config["init_image"] = attachment_lookup_url.get(config["init_image"])
        if config.get("interpolation_init_images"):
            config["interpolation_init_images"] = [
                attachment_lookup_url.get(img)
                for img in config["interpolation_init_images"]
            ]

    return response
