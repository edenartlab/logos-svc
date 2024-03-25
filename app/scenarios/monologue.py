from ..mongo import get_character_data
from ..llm import LLM
from ..prompt_templates import monologue_template, dialogue_template
from ..models import MonologueRequest, MonologueResult


def monologue(request: MonologueRequest) -> MonologueResult:
    params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

    character_data = get_character_data(request.character_id)
    name = character_data.get("name")
    description = character_data.get("logosData").get("identity")

    system_message = monologue_template.substitute(name=name, description=description)
    llm = LLM(model=request.model, system_message=system_message, params=params)
    monologue_text = llm(request.prompt, image=request.init_image)

    result = MonologueResult(monologue=monologue_text)

    return result
