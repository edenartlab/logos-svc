from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ..mongo import get_character_data
from ..llm import LLM
from ..character import EdenCharacter
from ..models import (
    StoryRequest, 
    StoryClip, 
    StoryResult
)
from ..prompt_templates.cinema import (
    screenwriter_system_template,
    screenwriter_prompt_template,
)


def story(request: StoryRequest):
    params = {"temperature": 1.0, "max_tokens": 4096, **request.params}

    character_details = ""
    character_names = []
    for character_id in request.character_ids:
        if character_id == "":
            continue
        character = EdenCharacter(character_id)
        character_names.append(character.name)
        character_details += character.card()
    
    story_prompt = request.prompt
    if character_details:
        character_details = f"Characters:\n{character_details}\n\nCharacter names (only use these for character field in each clip):\n{', '.join(character_names)}\n---\n\n"

    prompt = screenwriter_prompt_template.substitute(
        character_details=character_details,
        story=story_prompt,
    ).strip()

    screenwriter = LLM(
        model=request.model,
        system_message=screenwriter_system_template.template,
        params=params,
    )
    
    story = screenwriter(prompt, output_schema=StoryResult)
    
    print(story)
    #story["music_prompt"] = None
    #if not request.music:
    #    story["music_prompt"] = None

    print(request)
    # if request.music:
    #     if request.music_prompt:
    #         story["music_prompt"] = request.music_prompt
    #     else:
    #         story["music_prompt"] = "a long vibraphone solo"
        
            
    print("===== generate a story =======")
    print(prompt)
    print("-----")
    print(story)
    print("-----")

    return story
