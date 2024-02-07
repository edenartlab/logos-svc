from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ..mongo import get_character_data
from ..llm import LLM
from ..models import StoryRequest, StoryClip, StoryResult
from ..character import EdenCharacter
from ..prompt_templates.cinema import (
    screenwriter_system_template,
    screenwriter_prompt_template,
)


def story(request: StoryRequest):    
    params = {"temperature": 1.0, "max_tokens": 4096, **request.params}
    
    character_details = ""
    character_names = []
    for character_id in request.character_ids:
        character = EdenCharacter(character_id)
        character_names.append(character.name)
        character_details += character.card()
    
    # CharacterName = Enum("CharacterName", {
    #     name: name for name in character_names
    # })
        
    # class DynamicStoryClip(StoryClip):
    #     """
    #     A single clip in a screenplay sequence
    #     """
    #     character: Optional[CharacterName] = Field(description="Character name if voiceover mode is character, otherwise null (possible values: {})".format(", ".join(character_names)))

    # class DynamicStoryResult(BaseModel):
    #     """
    #     A screenplay consisting of a sequence of clips
    #     """
    #     clips: List[DynamicStoryClip] = Field(description="Clips in the sequence")

    prompt = screenwriter_prompt_template.substitute(
        character_details=character_details,
        character_names=", ".join(character_names),
        story=request.prompt,
    )

    screenwriter = LLM(
        model=request.model,
        system_message=screenwriter_system_template.template,
        params=params,
    )
    
    story = screenwriter(prompt, output_schema=StoryResult)
    
    print("===== generate a story =======")
    print(prompt)
    print("-----")
    print(story)
    print("-----")

    return story
