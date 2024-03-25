import re
import orjson
import random
import asyncio
from bson import ObjectId
from enum import Enum
from typing import List, Optional
from pydantic import Field, BaseModel, ValidationError

from .mongo import get_character_data
from .scenarios.tasks import summary
from .llm import LLM
from .mongo import search_character
from .models import (
    SummaryRequest,
    ChatMessage,
    Thought,
    GeneratorMode,
    Config,
    StoryNamedCharacters,
    StoryConfig,
    StoryCreatorOutput,
    CreatorOutput,
    CreatorInput,
    StoryCreatorInput,
)
from .prompt_templates.assistant import (
    identity_template,
    router_template,
    reply_template,
    chat_template,
    qa_template,
    creator_template,
    story_context_system,
    story_context_prompt_template,
    story_editor_system_template,
    story_editor_prompt_template,
)

character_card = """---
Name: {name}
Description: {identity}
"""


class Character:
    def __init__(
        self,
        name="AI",
        identity="You are a friendly assistant.",
        knowledge_summary=None,
        knowledge=None,
        creation_enabled=False,
        story_creation_enabled=False,
        concept=None,
        smart_reply=False,
        chat_model="gpt-3.5-turbo",
        image=None,
        voice=None,
    ):
        self.reply_params = {"temperature": 0.0, "max_tokens": 10}
        self.router_params = {"temperature": 0.0, "max_tokens": 10}
        self.creator_params = {"temperature": 0.1, "max_tokens": 1000}
        self.story_editor_params = {"temperature": 0.1, "max_tokens": 2000}
        self.story_context_params = {"temperature": 0.0, "max_tokens": 200}
        self.qa_params = {"temperature": 0.2, "max_tokens": 1000}
        self.chat_params = {"temperature": 0.9, "max_tokens": 1000}

        self.reply = LLM(params=self.reply_params)
        self.router = LLM(params=self.router_params)
        self.creator = LLM(params=self.creator_params)
        self.story_editor = LLM(params=self.story_editor_params)
        self.story_context = LLM(params=self.story_context_params)
        self.qa = LLM(params=self.qa_params)
        self.chat = LLM(params=self.chat_params)

        self.knowledge_summary = ""

        self.update(
            name=name,
            identity=identity,
            knowledge_summary=knowledge_summary,
            knowledge=knowledge,
            creation_enabled=creation_enabled,
            story_creation_enabled=story_creation_enabled,
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
        story_creation_enabled=False,
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
        self.story_creation_enabled = story_creation_enabled
        self.concept = concept
        self.smart_reply = False  # smart_reply  # disabled until ready
        self.chat_model = chat_model
        self.image = image
        self.voice = voice
        self.function_map = {"1": self._chat_}
        options = [
            "Regular conversation, chat, humor, small talk, or a asking for a question or comment about an attached image",
        ]

        if knowledge:
            if not self.knowledge_summary.strip():
                self.knowledge_summary = summary(SummaryRequest(text=self.knowledge))
            options.append("A question about or reference to your knowledge")
            knowledge_summary = (
                f"You have the following knowledge: {self.knowledge_summary}"
            )
            self.function_map[str(len(options))] = self._qa_

        if creation_enabled:
            options.append(
                "A request for an image or simple video creation that isn't a story",
            )
            self.function_map[str(len(options))] = self._create_

        if story_creation_enabled:
            options.append(
                "A request to help write or draft a story, or to animate a finished story or turn it into a movie or film.",
            )
            self.function_map[str(len(options))] = self._story_create_

        if len(options) == 1:
            self.router_prompt = ""
        else:
            options_prompt = ""
            for i, option in enumerate(options):
                options_prompt += f"{i+1}. {option}\n"
            self.router_prompt = router_template.substitute(
                knowledge_summary=knowledge_summary or "",
                options=options_prompt,
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

        self.story_context_system = story_context_system

        self.story_editor_system = story_editor_system_template.substitute(
            name=name,
            identity=identity,
        )

        self.router.update(system_message=self.router_prompt)
        self.creator.update(system_message=self.creator_prompt)
        self.story_context.update(system_message=self.story_context_system)
        self.story_editor.update(system_message=self.story_editor_system)
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
            f"Story Creation Enabled: {truncate(str(self.story_creation_enabled))}\n"
            f"Concept: {truncate(str(self.concept))}\n"
            f"Smart Reply: {truncate(str(self.smart_reply))}\n"
            f"Image: {truncate(str(self.image))}\n"
            f"Voice: {truncate(str(self.voice))}"
        )

    def card(self):
        return character_card.format(name=self.name, identity=self.identity)

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
        router_prompt += f"Me: {message.message}"
        router_prompt = router_prompt[-5000:]  # limit to 5000 characters
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
            image=message.attachments[0] if message.attachments else None,
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

    def _story_create_(
        self,
        message,
        session_id=None,
    ) -> dict:

        characters = (
            self.story_context.memory(
                "characters",
                session_id=session_id,
            )
            or {}
        )

        character_names = [c.lower() for c in characters]

        story_context_prompt = story_context_prompt_template.substitute(
            character_names=", ".join(character_names),
            message=message.message,
        )

        class ContextOutput(BaseModel):
            """
            Any new names listed by the user
            """

            new_names: List[str] = []

        response = self.story_context(
            prompt=story_context_prompt,
            id=session_id,
            output_schema=ContextOutput,
            model="gpt-3.5-turbo",
        )

        new_names = [
            name
            for name in response["new_names"]
            if name.lower() not in character_names
        ]

        for name in new_names:
            character = search_character(name)
            if character:
                characters[name] = EdenCharacter(str(character["_id"]))

        self.story_context.memory(
            "characters",
            session_id=session_id,
            value=characters,
        )

        additional_context = "Take into account this additional background information about some of the characters mentioned in the story:"
        for name, character in characters.items():
            additional_context += f"\n---\n{name}: {character.identity}\n"

        draft = (
            self.story_context.memory(
                "draft",
                session_id=session_id,
            )
            or "none"
        )

        story_editor_prompt = story_editor_prompt_template.substitute(
            draft=draft,
            additional_context=additional_context,
            message=message.message,
        )

        class StoryEditorOutput(BaseModel):
            """
            Response from the story editor
            """

            new_draft: str
            message: str
            request_animation: bool

        response = self.story_editor(
            prompt=story_editor_prompt,
            id=session_id,
            # input_schema=CreatorInput,
            output_schema=StoryEditorOutput,
            model="gpt-4-1106-preview",
            # model="gpt-3.5-turbo",
        )

        draft = self.story_context.memory(
            "draft",
            session_id=session_id,
            value=response.get("new_draft"),
        )

        request_animation = response.get("request_animation", False)

        message_out = response.get("message")

        if request_animation:
            characterIds = [characters[c].character_id for c in characters]

            config = {
                "generator": "story",
                "characterIds": characterIds,
                "prompt": draft,
                "num_clips": 10,
            }

        else:
            message_out += "\n\nHere is the current working draft:\n\n" + draft
            config = None

        message_in = message.message
        if message.attachments:
            message_in += f"\n\nAttachments: {message.attachments}"

        user_message = ChatMessage(role="user", content=message_in)
        assistant_message = ChatMessage(role="assistant", content=message_out)

        output = {"message": message_out, "config": config}

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
                self.story_context.new_session(
                    id=session_id,
                    system=self.story_context_system,
                    params=self.story_context_params,
                )
                self.story_editor.new_session(
                    id=session_id,
                    system=self.story_editor_system,
                    params=self.story_editor_params,
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
            message,
            session_id=session_id,
        )

        self.router.add_messages(user_message, assistant_message, id=session_id)
        self.creator.add_messages(user_message, assistant_message, id=session_id)
        self.story_editor.add_messages(user_message, assistant_message, id=session_id)
        self.story_context.add_messages(user_message, assistant_message, id=session_id)
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
        """
        Sync the character data from the database
        """

        character_data = get_character_data(self.character_id)
        logos_data = character_data.get("logosData")
        name = character_data.get("name")
        identity = logos_data.get("identity")
        knowledge_summary = logos_data.get("knowledgeSummary")
        knowledge = logos_data.get("knowledge")
        concept = logos_data.get("concept")
        abilities = logos_data.get("abilities")
        creation_enabled = abilities.get("creations", False) if abilities else False
        story_creation_enabled = (
            abilities.get("story_creations", False) if abilities else False
        )
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
            story_creation_enabled=story_creation_enabled,
            concept=concept,
            smart_reply=smart_reply,
            chat_model=chat_model,
            image=image,
            voice=voice,
        )

    def __call__(self, message, session_id=None):
        self.sync()
        return super().__call__(message, session_id)
