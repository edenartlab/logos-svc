from string import Template
from pathlib import Path

dir_path = Path(__file__).parent

with open(dir_path / 'screenwriter.txt', 'r') as file:
    screenwriter_template = Template(file.read())

with open(dir_path / 'director.txt', 'r') as file:
    director_template = Template(file.read())

with open(dir_path / 'cinematographer.txt', 'r') as file:
    cinematographer_template = Template(file.read())
