from ..mongo import get_character_data
from ..llm import LLM
from ..prompt_templates import monologue_template, dialogue_template
from ..models import DialogueRequest, DialogueResult


def dialogue(request: DialogueRequest):
    params = {"temperature": 1.0, "max_tokens": 1000, **request.params}

    characters = [
        get_character_data(character_id) 
        for character_id in request.character_ids
    ]

    llms = []
    for c, character in enumerate(characters):
        other_character = characters[(c + 1) % 2]
        system_message = dialogue_template.substitute(
            name=character.get("name"),
            description=character.get("logosData").get("identity"),
            other_name=other_character.get("name"),
            other_description=other_character.get("logosData").get("identity"),
            prompt=request.prompt,
        )
        llms.append(
            LLM(model=request.model, system_message=system_message, params=params)
        )

    message = "You are beginning the conversation. What is the first thing you say? Just the line. No quotes, no name markers."

    conversation = []

    for m in range(6):
        llm = llms[m % 2]
        message = llm(message)

        if not message:
            raise Exception("No response from character")

        conversation.append({
            "character_id": request.character_ids[m % 2], 
            "message": message
        })

    result = DialogueResult(dialogue=conversation)

    return result
