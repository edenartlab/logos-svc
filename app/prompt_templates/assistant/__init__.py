from string import Template
from pathlib import Path

dir_path = Path(__file__).parent

with open(dir_path / 'identity.txt', 'r') as file:
    identity_template = Template(file.read())

with open(dir_path / 'router.txt', 'r') as file:
    router_template = Template(file.read())

with open(dir_path / 'reply.txt', 'r') as file:
    reply_template = Template(file.read())

with open(dir_path / 'chat.txt', 'r') as file:
    chat_template = Template(file.read())

with open(dir_path / 'qa.txt', 'r') as file:
    qa_template = Template(file.read())

with open(dir_path / 'creator.txt', 'r') as file:
    creator_template = Template(file.read())


with open(dir_path / 'story_editor_system.txt', 'r') as file:
    story_editor_system_template = Template(file.read())

with open(dir_path / 'story_editor_prompt.txt', 'r') as file:
    story_editor_prompt_template = Template(file.read())

with open(dir_path / 'story_context_system.txt', 'r') as file:
    story_context_system = file.read()

with open(dir_path / 'story_context_prompt.txt', 'r') as file:
    story_context_prompt_template = Template(file.read())


with open(dir_path / 'livecoder_system.txt', 'r') as file:
    livecoder_system = Template(file.read())

with open(dir_path / 'livecoder_prompt.txt', 'r') as file:
    livecoder_prompt_template = Template(file.read())
