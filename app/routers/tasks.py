from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..llm import LLM
from ..prompt_templates import summary_template, moderation_template

router = APIRouter()


class SummaryRequest(BaseModel):
    text: str
    model: str = "gpt-4-1106-preview"

class SummaryResult(BaseModel):
    summary: str

@router.post("/tasks/summary")
def summary(request: SummaryRequest) -> SummaryResult:
    params = {"temperature": 0.0, "max_tokens": 1000}

    summary_message = summary_template.substitute(text=request.text)

    llm = LLM(model=request.model, params=params)
    message = llm(summary_message)

    result = SummaryResult(summary=message)

    return result


class ModerationRequest(BaseModel):
    text: str
    model: str = "gpt-3.5-turbo"

class ModerationResult(BaseModel):
    """
    Moderation scores for each category
    """
    nsfw: int = Field(description="Sexually explicit or nudity")
    gore: int = Field(description="Violence or gore")
    hate: int = Field(description="Hate, abusive or toxic speech")

@router.post("/tasks/moderation")
def moderation(request: ModerationRequest) -> ModerationResult:
    params = {"temperature": 0.0, "max_tokens": 1000}

    system_message = moderation_template.template
    content = request.text

    llm = LLM(model=request.model, system_message=system_message, params=params)
    result = llm(content, output_schema=ModerationResult)

    return result
