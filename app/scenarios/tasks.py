from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..llm import LLM
from ..prompt_templates import summary_template, moderation_template
from ..models import (
    SummaryRequest, 
    ModerationRequest, 
    ModerationResult,
    SimpleAssistantRequest
)


def summary(request: SummaryRequest) -> str:
    params = {"temperature": 0.0, "max_tokens": 1000}

    summary_message = summary_template.substitute(text=request.text)

    llm = LLM(model=request.model, params=params)
    result = llm(summary_message)

    return result


def moderation(request: ModerationRequest) -> ModerationResult:
    params = {"temperature": 0.0, "max_tokens": 1000, **request.params}

    system_message = moderation_template.template
    content = request.text

    llm = LLM(model=request.model, system_message=system_message, params=params)
    result = llm(content, output_schema=ModerationResult)

    return result


def general_assistant(request: SimpleAssistantRequest) -> str:
    params = {"temperature": 0.0, "max_tokens": 1000, **request.params}
    
    llm = LLM(model=request.model, params=params)
    result = llm(request.prompt, output_schema=request.output_schema)
    
    if request.output_schema is not None:
        return result[request.output_schema.__name__]
    else:
        return result
