import re
import orjson
import random
import asyncio
from enum import Enum
from typing import List, Optional
from pydantic import Field, BaseModel, ValidationError

from .mongo import get_character_data
from .scenarios.tasks import summary
from .llm import LLM
from .models import SummaryRequest, ChatMessage
from .prompt_templates.assistant import (
    identity_template,
    reply_template,
    chat_template,
    creator_template,
    qa_template,
    router_template,
)


class Thought(BaseModel):
    """
    Probability percentage that the character responds to the conversation
    """

    probability: str = Field(
        description="A percentage chance that the character will respond to the conversation"
    )


class GeneratorMode(Enum):
    create = "create"
    controlnet = "controlnet"
    interpolate = "interpolate"
    real2real = "real2real"
    remix = "remix"
    blend = "blend"
    upscale = "upscale"


class Config(BaseModel):
    """
    JSON config for Eden generator request
    """

    generator: GeneratorMode = Field(description="Which generator to use")
    text_input: Optional[str] = Field(description="Text prompt that describes image")
    seed: Optional[int] = Field(description="Seed for random number generator")
    init_image: Optional[str] = Field(
        description="Path to image file for create, remix, or upscale"
    )
    init_image_strength: Optional[float] = Field(
        description="Strength of init image, default 0.15"
    )
    control_image: Optional[str] = Field(
        description="Path to image file for controlnet"
    )
    control_image_strength: Optional[float] = Field(
        description="Strength of control image for controlnet, default 0.6"
    )
    interpolation_init_images: Optional[List[str]] = Field(
        description="List of paths to image files for real2real or blend"
    )
    interpolation_texts: Optional[List[str]] = Field(
        description="List of text prompts for interpolate"
    )
    interpolation_seeds: Optional[List[int]] = Field(
        description="List of seeds for interpolation texts"
    )
    n_frames: Optional[int] = Field(description="Number of frames in output video")


class CreatorOutput(BaseModel):
    """
    Output of creator LLM containing a JSON config and a message to the user
    """

    config: Config = Field(description="Config for Eden generator")
    message: str = Field(description="Message to user")


class CreatorInput(BaseModel):
    """
    Input to creator LLM containing a prompt, and optionally a list of attachments
    """

    message: str = Field(description="Message to LLM")
    attachments: Optional[List[str]] = Field(
        default_factory=list, description="List of file paths to attachments"
    )


class Character:
    def __init__(
        self,
        name="AI",
        identity="You are a friendly assistant.",
        knowledge_summary=None,
        knowledge=None,
        creation_enabled=False,
        concept=None,
        smart_reply=False,
        chat_model="gpt-3.5-turbo",
        image=None,
        voice=None,
    ):
        self.reply_params = {"temperature": 0.0, "max_tokens": 10}
        self.router_params = {"temperature": 0.0, "max_tokens": 10}
        self.creator_params = {"temperature": 0.1, "max_tokens": 1000}
        self.qa_params = {"temperature": 0.2, "max_tokens": 1000}
        self.chat_params = {"temperature": 0.9, "max_tokens": 1000}

        self.reply = LLM(params=self.reply_params)
        self.router = LLM(params=self.router_params)
        self.creator = LLM(params=self.creator_params)
        self.qa = LLM(params=self.qa_params)
        self.chat = LLM(params=self.chat_params)

        self.knowledge_summary = ""
        
        self.update(
            name=name,
            identity=identity,
            knowledge_summary=knowledge_summary,
            knowledge=knowledge,
            creation_enabled=creation_enabled,
            concept=concept,
            smart_reply=smart_reply,
            chat_model=chat_model,
            image=image,
            voice=voice,
        )

    def update(
        self,
        name,
        identity,
        knowledge_summary=None,
        knowledge=None,
        creation_enabled=False,
        concept=None,
        smart_reply=False,
        chat_model="gpt-3.5-turbo",
        image=None,
        voice=None,
    ):
        self.name = name
        self.identity = identity
        if knowledge_summary:
            self.knowledge_summary = knowledge_summary
        self.knowledge = knowledge
        self.creation_enabled = creation_enabled
        self.concept = concept
        self.smart_reply = smart_reply
        self.chat_model = chat_model
        self.image = image
        self.voice = voice
        self.function_map = {"1": self._chat_}
        options = ["Regular conversation, chat, humor, or small talk"]

        if knowledge:
            if not self.knowledge_summary.strip():
                self.knowledge_summary = summary(
                    SummaryRequest(text=self.knowledge)
                ).summary
            options.append("A question about or reference to your knowledge")
            knowledge_summary = (
                f"You have the following knowledge: {self.knowledge_summary}"
            )
            self.function_map[str(len(options))] = self._qa_
        
        if creation_enabled:
            options.append("A request for an image or video creation")
            self.function_map[str(len(options))] = self._create_

        if len(options) == 1:
            self.router_prompt = ""
        else:
            options_prompt = ""
            for i, option in enumerate(options):
                options_prompt += f"{i+1}. {option}\n"
            self.router_prompt = router_template.substitute(
                knowledge_summary=knowledge_summary or "", options=options_prompt
            )

        self.identity_prompt = identity_template.substitute(
            name=name,
            identity=identity,
        )

        self.chat_prompt = chat_template.substitute(
            name=name,
            identity=identity,
        )

        self.qa_prompt = qa_template.substitute(
            name=name,
            identity=identity,
            knowledge=knowledge,
        )

        self.creator_prompt = creator_template.substitute(
            name=name,
            identity=identity,
        )

        self.router.update(system_message=self.router_prompt)
        self.creator.update(system_message=self.creator_prompt)
        self.qa.update(system_message=self.qa_prompt)
        self.chat.update(system_message=self.chat_prompt)
        self.reply.update(system_message=self.identity_prompt)

    def __str__(self):
        def truncate(s):
            return (s[:47] + "...") if len(s) > 50 else s

        return (
            f"Name: {truncate(self.name)}\n"
            f"Identity: {truncate(self.identity)}\n"
            f"Knowledge Summary: {truncate(str(self.knowledge_summary))}\n"
            f"Knowledge: {truncate(str(self.knowledge))}\n"
            f"Creation Enabled: {truncate(str(self.creation_enabled))}\n"
            f"Concept: {truncate(str(self.concept))}\n"
            f"Smart Reply: {truncate(str(self.smart_reply))}\n"
            f"Image: {truncate(str(self.image))}\n"
            f"Voice: {truncate(str(self.voice))}"
        )

    def think(
        self,
        message,
    ) -> bool:
        if not self.smart_reply:
            return False

        user_message = reply_template.substitute(
            chat=message,
        )
        result = self.reply(
            prompt=user_message, 
            output_schema=Thought, 
            save_messages=False,
            model="gpt-4-1106-preview",
        )

        probability = result["probability"]
        probability = float(probability.replace("%", "").strip()) / 100
        R = random.random()

        return R < probability

    def _route_(
        self,
        message,
        session_id=None,
    ) -> dict:
        conversation = self.chat.get_messages(id=session_id)
        router_prompt = "What is the most relevant category for the last message, in the context of this conversation?\n\n"
        for msg in conversation:
            role = "Eden" if msg.role == "assistant" else "Me"
            router_prompt += f"{role}: {msg.content}\n"
        router_prompt += f"Me: {message.message}\n"
        index = self.router(
            prompt=router_prompt, 
            save_messages=False,
            model="gpt-4-1106-preview",
        )
        match = re.match(r"-?\d+", index)
        if match:
            index = match.group()
            return index
        else:
            return None

    def _chat_(
        self,
        message,
        session_id=None,
    ) -> dict:
        response = self.chat(
            prompt=message.message, 
            id=session_id, 
            save_messages=False,
            model=self.chat_model,
        )
        user_message = ChatMessage(role="user", content=message.message)
        assistant_message = ChatMessage(role="assistant", content=response)
        output = {"message": response, "config": None}
        return output, user_message, assistant_message

    def _qa_(self, message, session_id=None) -> dict:
        response = self.qa(
            prompt=message.message, 
            id=session_id, 
            save_messages=False,
            model=self.chat_model,
        )
        user_message = ChatMessage(role="user", content=message.message)
        assistant_message = ChatMessage(role="assistant", content=response)
        output = {"message": response, "config": None}
        return output, user_message, assistant_message

    def _create_(
        self,
        message,
        session_id=None,
    ) -> dict:
        response = self.creator(            
            prompt=message,
            id=session_id,
            input_schema=CreatorInput,
            output_schema=CreatorOutput,
            model="gpt-4-1106-preview",
        )

        config = {k: v for k, v in response["config"].items() if v}

        # add concept if set
        if self.concept:
            config["lora"] = self.concept
            config["lora_scale"] = 0.6

        # insert seeds if not provided
        if config.get("interpolation_texts"):
            if not config.get("interpolation_seeds"):
                config["interpolation_seeds"] = [
                    random.randint(0, 1000000) for _ in config["interpolation_texts"]
                ]
        elif not config.get("seed"):
            config["seed"] = random.randint(0, 1000000)

        message_out = response["message"]
        if config:
            message_out += f"\nConfig: {config}"

        message_in = message.message
        if message.attachments:
            message_in += f"\n\nAttachments: {message.attachments}"

        user_message = ChatMessage(role="user", content=message_in)
        assistant_message = ChatMessage(role="assistant", content=message_out)

        output = {"message": response.get("message"), "config": config}

        return output, user_message, assistant_message

    def __call__(
        self,
        message,
        session_id=None,
    ) -> dict:
        message = CreatorInput.model_validate(message)

        if session_id:
            if session_id not in self.router.sessions:
                self.router.new_session(
                    id=session_id,
                    system=self.router_prompt,
                    params=self.router_params,
                )
                self.creator.new_session(
                    id=session_id,
                    system=self.creator_prompt,
                    params=self.creator_params,
                )
                self.qa.new_session(
                    id=session_id,
                    system=self.qa_prompt,
                    params=self.qa_params,
                )
                self.chat.new_session(
                    id=session_id,
                    system=self.chat_prompt,
                    params=self.chat_params,
                )

        function = None
        if self.router_prompt:
            index = self._route_(message, session_id=session_id)
            function = self.function_map.get(index)

        if not function:
            function = self.function_map.get("1")

        output, user_message, assistant_message = function(
            message, session_id=session_id
        )

        self.router.add_messages(user_message, assistant_message, id=session_id)
        self.creator.add_messages(user_message, assistant_message, id=session_id)
        self.qa.add_messages(user_message, assistant_message, id=session_id)
        self.chat.add_messages(user_message, assistant_message, id=session_id)

        return output


class EdenCharacter(Character):
    def __init__(
        self,
        character_id,
    ):
        super().__init__()
        self.character_id = character_id
        self.sync()

    def sync(self):
        character_data = get_character_data(self.character_id)
        logos_data = character_data.get("logosData")
        name = character_data.get("name")
        identity = logos_data.get("identity")
        knowledge_summary = logos_data.get("knowledgeSummary")
        knowledge = logos_data.get("knowledge")
        concept = logos_data.get("concept")
        abilities = logos_data.get("abilities")
        creation_enabled = abilities.get("creations", True) if abilities else True
        smart_reply = abilities.get("smart_reply", False) if abilities else False
        chat_model = logos_data.get("chatModel", "gpt-4-1106-preview")
        image = character_data.get("image")
        voice = character_data.get("voice")

        self.update(
            name=name,
            identity=identity,
            knowledge_summary=knowledge_summary,
            knowledge=knowledge,
            creation_enabled=creation_enabled,
            concept=concept,
            smart_reply=smart_reply,
            chat_model=chat_model,
            image=image,
            voice=voice,
        )
