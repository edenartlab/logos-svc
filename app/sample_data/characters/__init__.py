import glob
from pathlib import Path

from ...models import Character

def read_file(subfolder, filename):
    dir_path = Path(__file__).parent
    filepath = dir_path / subfolder / filename
    if not filepath.exists():
        return None
    with open(filepath, 'r') as file:
        return file.read()


eden_assistant = Character(
    name="Eden Assistant",
    description=read_file("eden", "description.txt"),
    knowledge_summary=read_file("eden", "knowledge_summary.txt"),
    knowledge=read_file("eden", "knowledge.txt"),
    image="",
    voice="",
)

alice = Character(
    name="Alice",
    description=read_file("alice", "description.txt"),
    knowledge_summary=read_file("alice", "knowledge_summary.txt"),
    knowledge=read_file("alice", "knowledge.txt"),
    image="",
    voice="",
)

bob = Character(
    name="Bob",
    description=read_file("bob", "description.txt"),
    knowledge_summary=read_file("bob", "knowledge_summary.txt"),
    knowledge=read_file("bob", "knowledge.txt"),
    image="",
    voice="",
)