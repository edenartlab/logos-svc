from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ..mongo import get_character_data
from ..llm import LLM
from ..character import EdenCharacter
from ..models import (
    ReelRequest, 
    ReelResult
)
from ..prompt_templates.cinema import (
    reelwriter_system_template,
    reelwriter_prompt_template,
)


def reel(request: ReelRequest):
    params = {"temperature": 1.0, "max_tokens": 4096, **request.params}

    character_details = ""
    character_names = []
    for character_id in request.character_ids:
        if character_id == "":
            continue
        character = EdenCharacter(character_id)
        character_names.append(character.name)
        character_details += character.card()
    
    prompt = reelwriter_prompt_template.substitute(
        character_details=character_details,
        character_names=", ".join(character_names),
        prompt=request.prompt,
    )

    reelwriter = LLM(
        model=request.model,
        system_message=reelwriter_system_template.template,
        params=params,
    )
    
    reel_result = reelwriter(prompt, output_schema=ReelResult)
    
    print("===== generate a reel =======")
    print(prompt)
    print("-----")
    print(reel_result)
    print("-----")

    return reel_result
