from fastapi import APIRouter
from pydantic import BaseModel

from ..llm import LLM
from ..prompt_templates import summary_template

router = APIRouter()


class SummaryRequest(BaseModel):
    text: str
    model: str = "gpt-4-1106-preview"

class SummaryResult(BaseModel):
    summary: str

@router.post("/summary")
async def summary(request: SummaryRequest) -> SummaryResult:
    params = {"temperature": 0.0, "max_tokens": 1000}

    summary_message = summary_template.substitute(text=request.text)
    print(summary_message)

    llm = LLM(model=request.model, params=params)
    message = llm(summary_message)

    result = SummaryResult(summary=message)

    return result
