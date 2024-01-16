from ..mongo import get_character_data
from ..llm import LLM
from ..models import StoryRequest, StoryResult
from ..character import EdenCharacter
from ..prompt_templates.cinema import (
    screenwriter_system_template,
    screenwriter_prompt_template,
    #director_template,
    #cinematographer_template,
)


def story(request: StoryRequest) -> StoryResult:
    params = {"temperature": 1.0, "max_tokens": 1000, **request.params}
    
    screenwriter = LLM(
        model=request.model,
        system_message=str(screenwriter_system_template),
        params=params,
    )

    character_details = ""
    for character_id in request.character_ids:
        character = EdenCharacter(character_id)
        character_detail = f"""---
    Name: {character.name}
    Description: {character.identity}
    
    """
        character_details += character_detail

    prompt = screenwriter_prompt_template.substitute(
        character_details=character_details,
        story=request.prompt,
    )

    story = screenwriter(prompt, output_schema=StoryResult)
    
    return story
