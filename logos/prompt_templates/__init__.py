from string import Template
from pathlib import Path

from . import assistant
from . import cinema

dir_path = Path(__file__).parent

with open(dir_path / "monologue.txt", "r") as file:
    monologue_template = Template(file.read())

with open(dir_path / "dialogue.txt", "r") as file:
    dialogue_template = Template(file.read())

with open(dir_path / "identity.txt", "r") as file:
    identity_template = Template(file.read())

with open(dir_path / "summary.txt", "r") as file:
    summary_template = Template(file.read())

with open(dir_path / "moderation.txt", "r") as file:
    moderation_template = Template(file.read())
