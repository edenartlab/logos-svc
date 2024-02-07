import os
from pydantic import BaseModel, SecretStr, HttpUrl, Field
from uuid import uuid4, UUID
from httpx import Client, AsyncClient
from typing import List, Dict, Union, Set, Any, Optional
import orjson
import datetime

from ..models import ChatMessage
from ..utils import remove_a_key, now_tz


ALLOWED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4-1106-preview",
    "gryphe/mythomax-l2-13b-8k",
    "mistralai/mistral-medium",
    "mistralai/mixtral-8x7b-instruct",
    "nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
    "nousresearch/nous-capybara-7b",
    "teknium/openhermes-2-mistral-7b",
    "pygmalionai/mythalion-13b",
    "anthropic/claude-2",
    "cognitivecomputations/dolphin-mixtral-8x7b"
]

OPENAI_API_URL: HttpUrl = "https://api.openai.com/v1/chat/completions"
OPENROUTER_API_URL: HttpUrl = "https://openrouter.ai/api/v1/chat/completions"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

assert OPENAI_API_KEY, f"An API key for OpenAI was not defined."
assert OPENROUTER_API_KEY, f"An API key for OpenRouter was not defined."


tool_prompt = """From the list of tools below:
- Reply ONLY with the number of the tool appropriate in response to the user's last message.
- If no tool is appropriate, ONLY reply with \"0\".

{tools}"""


class ChatSession(BaseModel):
    id: Union[str, UUID] = Field(default_factory=uuid4)
    created_at: datetime.datetime = Field(default_factory=now_tz)
    auth: Dict[str, SecretStr] = {}
    system: str = "You are a helpful assistant."
    params: Dict[str, Any] = {"temperature": 0.7}
    messages: List[ChatMessage] = []
    input_fields: Set[str] = {"role", "content", "name"}
    recent_messages: Optional[int] = None
    save_messages: Optional[bool] = True
    memory: Dict[str, Any] = {}
    total_prompt_length: int = 0
    total_completion_length: int = 0
    total_length: int = 0
    title: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.auth: Dict[str, SecretStr] = {
            "openai_api_key": SecretStr(OPENAI_API_KEY),
            "openrouter_api_key": SecretStr(OPENROUTER_API_KEY),
        }

    def __str__(self) -> str:
        sess_start_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        last_message_str = self.messages[-1].received_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"""Chat session started at {sess_start_str}:
        - {len(self.messages):,} Messages
        - Last message sent at {last_message_str}"""

    def format_input_messages(
        self, system_message: ChatMessage, user_message: ChatMessage
    ) -> list:
        recent_messages = (
            self.messages[-self.recent_messages :]
            if self.recent_messages
            else self.messages
        )
        messages = (
            [system_message.model_dump(include=self.input_fields, exclude_none=True)]
            + [
                m.model_dump(include=self.input_fields, exclude_none=True)
                for m in recent_messages
            ]
        )
        if user_message:
            messages += [user_message.model_dump(include=self.input_fields, exclude_none=True)]
        return messages

    def add_messages(
        self,
        user_message: ChatMessage,
        assistant_message: ChatMessage,
        save_messages: bool = None,
    ) -> None:

        # if save_messages is explicitly defined, always use that choice
        # instead of the default
        to_save = isinstance(save_messages, bool)

        if to_save:
            if save_messages:
                self.messages.append(user_message)
                self.messages.append(assistant_message)
        elif self.save_messages:
            self.messages.append(user_message)
            self.messages.append(assistant_message)

    def prepare_request(
        self,
        model: str = "gpt-3.5-turbo",
        prompt: str = None,
        system: str = None,
        params: Dict[str, Any] = None,
        stream: bool = False,
        input_schema: Any = None,
        output_schema: Any = None,
        is_function_calling_required: bool = True,
    ):
        headers = {
            "Content-Type": "application/json"
        }

        if model not in ALLOWED_MODELS:
            raise ValueError(f"Invalid model: {model}. Available models: {ALLOWED_MODELS}")

        provider = "openai" if "gpt-" in model else "openrouter"

        if provider == "openai":
            api_url = OPENAI_API_URL
            headers["Authorization"] = f"Bearer {self.auth['openai_api_key'].get_secret_value()}"
        elif provider == "openrouter":
            api_url = OPENROUTER_API_URL
            headers["HTTP-Referer"] = "https://eden.art"
            headers["X-Title"] = "Eden.art"
            headers["Authorization"] = f"Bearer {self.auth['openrouter_api_key'].get_secret_value()}"
        else:
            raise ValueError(f"Unknown provider: {provider}")

        system_message = ChatMessage(role="system", content=system or self.system)
        user_message = None

        if prompt:
            if not input_schema:
                user_message = ChatMessage(role="user", content=prompt)
            else:
                assert isinstance(
                    prompt, input_schema
                ), f"prompt must be an instance of {input_schema.__name__}"
                user_message = ChatMessage(
                    role="function",
                    content=prompt.model_dump_json(),
                    name=input_schema.__name__,
                )

        gen_params = params or self.params
        data = {
            "model": model,
            "messages": self.format_input_messages(system_message, user_message),
            "stream": stream,
            **gen_params,
        }

        #print("------------------------------------------")
        #print(orjson.dumps(data, option=orjson.OPT_INDENT_2).decode())

        # Add function calling parameters if a schema is provided
        if input_schema or output_schema:
            functions = []
            if input_schema:
                input_function = self.schema_to_function(input_schema)
                functions.append(input_function)
            if output_schema:
                output_function = self.schema_to_function(output_schema)
                functions.append(
                    output_function
                ) if output_function not in functions else None
                if is_function_calling_required:
                    data["function_call"] = {"name": output_schema.__name__}
            data["functions"] = functions

        return api_url, headers, data, user_message

    def schema_to_function(self, schema: Any):
        assert schema.__doc__, f"{schema.__name__} is missing a docstring."
        assert (
            "title" not in schema.model_fields.keys()
        ), "`title` is a reserved keyword and cannot be used as a field name."
        schema_dict = schema.model_json_schema()
        remove_a_key(schema_dict, "title")

        return {
            "name": schema.__name__,
            "description": schema.__doc__,
            "parameters": schema_dict,
        }

    def gen(
        self,
        model: str,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
        input_schema: Any = None,
        output_schema: Any = None,
    ):
        api_url, headers, data, user_message = self.prepare_request(
            model, prompt, system, params, False, input_schema, output_schema
        )
        print("______________")
        print(data)
        print("______________")
        r = client.post(
            api_url,
            json=data,
            headers=headers,
            timeout=None,
        )
        r = r.json()

        try:
            if not output_schema:
                content = r["choices"][0]["message"]["content"]
                assistant_message = ChatMessage(
                    role=r["choices"][0]["message"]["role"],
                    content=content,
                    # finish_reason=r["choices"][0]["finish_reason"],
                    # prompt_length=r["usage"]["prompt_tokens"],
                    # completion_length=r["usage"]["completion_tokens"],
                    # total_length=r["usage"]["total_tokens"],
                )
                self.add_messages(user_message, assistant_message, save_messages)
            else:
                content = r["choices"][0]["message"]["function_call"]["arguments"]
                content = orjson.loads(content)

            # self.total_prompt_length += r["usage"]["prompt_tokens"]
            # self.total_completion_length += r["usage"]["completion_tokens"]
            # self.total_length += r["usage"]["total_tokens"]
        except KeyError:
            raise KeyError(f"No AI generation: {r}")
        
        return content

    def stream(
        self,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
        input_schema: Any = None,
    ):
        api_url, headers, data, user_message = self.prepare_request(
            prompt, system, params, True, input_schema
        )

        with client.stream(
            "POST",
            api_url,
            json=data,
            headers=headers,
            timeout=None,
        ) as r:
            content = []
            for chunk in r.iter_lines():
                if len(chunk) > 0:
                    chunk = chunk[6:]  # SSE JSON chunks are prepended with "data: "
                    if chunk != "[DONE]":
                        chunk_dict = orjson.loads(chunk)
                        delta = chunk_dict["choices"][0]["delta"].get("content")
                        if delta:
                            content.append(delta)
                            yield {"delta": delta, "response": "".join(content)}

        # streaming does not currently return token counts
        assistant_message = ChatMessage(
            role="assistant",
            content="".join(content),
        )

        self.add_messages(user_message, assistant_message, save_messages)

        return assistant_message

    def gen_with_tools(
        self,
        prompt: str,
        tools: List[Any],
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        # call 1: select tool and populate context
        tools_list = "\n".join(f"{i+1}: {f.__doc__}" for i, f in enumerate(tools))
        tool_prompt_format = tool_prompt.format(tools=tools_list)

        logit_bias_weight = 100
        logit_bias = {str(k): logit_bias_weight for k in range(15, 15 + len(tools) + 1)}

        tool_idx = int(
            self.gen(
                prompt,
                client=client,
                system=tool_prompt_format,
                save_messages=False,
                params={
                    "temperature": 0.0,
                    "max_tokens": 1,
                    "logit_bias": logit_bias,
                },
            )
        )

        # if no tool is selected, do a standard generation instead.
        if tool_idx == 0:
            return {
                "response": self.gen(
                    prompt,
                    client=client,
                    system=system,
                    save_messages=save_messages,
                    params=params,
                ),
                "tool": None,
            }
        selected_tool = tools[tool_idx - 1]
        context_dict = selected_tool(prompt)
        if isinstance(context_dict, str):
            context_dict = {"context": context_dict}

        context_dict["tool"] = selected_tool.__name__

        # call 2: generate from the context
        new_system = f"{system or self.system}\n\nYou MUST use information from the context in your response."
        new_prompt = f"Context: {context_dict['context']}\n\nUser: {prompt}"

        context_dict["response"] = self.gen(
            new_prompt,
            client=client,
            system=new_system,
            save_messages=False,
            params=params,
        )

        # manually append the nonmodified user message + normal AI response
        user_message = ChatMessage(role="user", content=prompt)
        assistant_message = ChatMessage(
            role="assistant", content=context_dict["response"]
        )
        self.add_messages(user_message, assistant_message, save_messages)

        return context_dict

    async def gen_async(
        self,
        model: str,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
        input_schema: Any = None,
        output_schema: Any = None,
    ):
        api_url, headers, data, user_message = self.prepare_request(
            model, prompt, system, params, False, input_schema, output_schema
        )

        r = await client.post(
            api_url,
            json=data,
            headers=headers,
            timeout=None,
        )
        r = r.json()

        try:
            if not output_schema:
                content = r["choices"][0]["message"]["content"]
                assistant_message = ChatMessage(
                    role=r["choices"][0]["message"]["role"],
                    content=content,
                    # finish_reason=r["choices"][0]["finish_reason"],
                    # prompt_length=r["usage"]["prompt_tokens"],
                    # completion_length=r["usage"]["completion_tokens"],
                    # total_length=r["usage"]["total_tokens"],
                )
                self.add_messages(user_message, assistant_message, save_messages)
            else:
                content = r["choices"][0]["message"]["function_call"]["arguments"]
                content = orjson.loads(content)

            # self.total_prompt_length += r["usage"]["prompt_tokens"]
            # self.total_completion_length += r["usage"]["completion_tokens"]
            # self.total_length += r["usage"]["total_tokens"]
        except KeyError:
            raise KeyError(f"No AI generation: {r}")

        return content

    async def stream_async(
        self,
        model: str,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
        input_schema: Any = None,
    ):
        api_url, headers, data, user_message = self.prepare_request(
            model, prompt, system, params, True, input_schema
        )

        async with client.stream(
            "POST",
            api_url,
            json=data,
            headers=headers,
            timeout=None,
        ) as r:
            content = []
            async for chunk in r.aiter_lines():
                if len(chunk) > 0:
                    chunk = chunk[6:]  # SSE JSON chunks are prepended with "data: "
                    if chunk != "[DONE]":
                        chunk_dict = orjson.loads(chunk)
                        delta = chunk_dict["choices"][0]["delta"].get("content")
                        if delta:
                            content.append(delta)
                            yield {"delta": delta, "response": "".join(content)}

        # streaming does not currently return token counts
        assistant_message = ChatMessage(
            role="assistant",
            content="".join(content),
        )

        self.add_messages(user_message, assistant_message, save_messages)

    async def gen_with_tools_async(
        self,
        prompt: str,
        tools: List[Any],
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        # call 1: select tool and populate context
        tools_list = "\n".join(f"{i+1}: {f.__doc__}" for i, f in enumerate(tools))
        tool_prompt_format = tool_prompt.format(tools=tools_list)

        logit_bias_weight = 100
        logit_bias = {str(k): logit_bias_weight for k in range(15, 15 + len(tools) + 1)}

        tool_idx = int(
            await self.gen_async(
                prompt,
                client=client,
                system=tool_prompt_format,
                save_messages=False,
                params={
                    "temperature": 0.0,
                    "max_tokens": 1,
                    "logit_bias": logit_bias,
                },
            )
        )

        # if no tool is selected, do a standard generation instead.
        if tool_idx == 0:
            return {
                "response": await self.gen_async(
                    prompt,
                    client=client,
                    system=system,
                    save_messages=save_messages,
                    params=params,
                ),
                "tool": None,
            }
        selected_tool = tools[tool_idx - 1]
        context_dict = await selected_tool(prompt)
        if isinstance(context_dict, str):
            context_dict = {"context": context_dict}

        context_dict["tool"] = selected_tool.__name__

        # call 2: generate from the context
        new_system = f"{system or self.system}\n\nYou MUST use information from the context in your response."
        new_prompt = f"Context: {context_dict['context']}\n\nUser: {prompt}"

        context_dict["response"] = await self.gen_async(
            new_prompt,
            client=client,
            system=new_system,
            save_messages=False,
            params=params,
        )

        # manually append the nonmodified user message + normal AI response
        user_message = ChatMessage(role="user", content=prompt)
        assistant_message = ChatMessage(
            role="assistant", content=context_dict["response"]
        )
        self.add_messages(user_message, assistant_message, save_messages)

        return context_dict
