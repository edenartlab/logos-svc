from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ..mongo import get_character_data
from ..llm import LLM
from ..character import EdenCharacter
from ..models import StoryRequest, StoryClip, StoryResult
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
        model="gpt-4o", #request.model,
        system_message=screenwriter_system_template.template,
        params=params,
    )

    # hack to do story type validation, fixed in eden2
    finished = False
    tries = 0
    max_tries = 5
    while not finished:
        try:
            story = screenwriter(prompt, output_schema=StoryResult)
            clip_keys = [c.keys() for c in story["clips"]]
            required_keys = {'voiceover', 'character', 'speech', 'image_prompt'}
            all_clips_valid = all(required_keys.issubset(set(clip)) for clip in clip_keys)
            if not all_clips_valid:
                print("Missing keys in clips")
                print(clip_keys)
                raise ValueError("One or more clips are missing required keys.")
            finished = True
            break
        except Exception as e:
            print("Error:", e)
            tries += 1
            if tries >= max_tries:
                raise Exception("Max tries exceeded...")

    #story = screenwriter(prompt, output_schema=StoryResult)

    if request.music:
        if request.music_prompt and request.music_prompt.strip():
            story["music_prompt"] = request.music_prompt  # override
    else:
        story["music_prompt"] = None

    print("===== generate a story =======")
    print(prompt)
    print("-----")
    print(story)
    print("-----")

    return story
