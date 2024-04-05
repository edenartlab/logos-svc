from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ..mongo import get_character_data
from ..llm import LLM
from ..character import EdenCharacter
from ..models import ReelNarrationMode, ReelRequest, ReelResult
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

    reel_prompt = request.prompt
    if request.narration == ReelNarrationMode.on:
        reel_prompt += (
            f"\n\nThe user has requested there should be a narrated voiceover."
        )
    elif request.narration == ReelNarrationMode.off:
        reel_prompt += (
            f"\n\nThe user has requested there should be **NO** narrated voiceover."
        )

    if character_details:
        character_details = f"Characters:\n{character_details}\n\nCharacter names (only use these for character field in each clip):\n{', '.join(character_names)}\n---\n\n"

    prompt = reelwriter_prompt_template.substitute(
        character_details=character_details,
        prompt=reel_prompt,
    ).strip()

    reelwriter = LLM(
        model=request.model,
        system_message=reelwriter_system_template.template,
        params=params,
    )

    reel_result = reelwriter(prompt, output_schema=ReelResult)

    if request.narration == ReelNarrationMode.on:
        reel_result["voiceover"] = "narrator"
        reel_result["character"] = request.narrator_id
    elif request.narration == ReelNarrationMode.off:
        reel_result["voiceover"] = "none"
        reel_result["character"] = None
        reel_result["speech"] = None

    if request.music_prompt:
        reel_result["music_prompt"] = request.music_prompt

    print("===== generate a reel =======")
    print(prompt)
    print("-----")
    print(reel_result)
    print("-----")

    return reel_result
