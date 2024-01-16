from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..llm import LLM
from ..prompt_templates import summary_template, moderation_template
from ..models import (
    SummaryRequest, 
    SummaryResult, 
    ModerationRequest, 
    ModerationResult
)


def summary(request: SummaryRequest) -> SummaryResult:
    params = {"temperature": 0.0, "max_tokens": 1000}

    summary_message = summary_template.substitute(text=request.text)

    llm = LLM(model=request.model, params=params)
    message = llm(summary_message)

    result = SummaryResult(summary=message)

    return result


def moderation(request: ModerationRequest) -> ModerationResult:
    params = {"temperature": 0.0, "max_tokens": 1000}

    system_message = moderation_template.template
    content = request.text

    llm = LLM(model=request.model, system_message=system_message, params=params)
    result = llm(content, output_schema=ModerationResult)

    return result
