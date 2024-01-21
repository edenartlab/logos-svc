from string import Template
from pathlib import Path

dir_path = Path(__file__).parent

with open(dir_path / 'comicwriter_system.txt', 'r') as file:
    comicwriter_system_template = Template(file.read())
