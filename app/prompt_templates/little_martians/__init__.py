from string import Template
from pathlib import Path
import json

dir_path = Path(__file__).parent

with open(dir_path / 'littlemartians_poster_system.txt', 'r') as file:
    littlemartians_poster_system = Template(file.read())

with open(dir_path / 'littlemartians_poster_prompt.txt', 'r') as file:
    littlemartians_poster_prompt = Template(file.read())

with open(dir_path / 'littlemartians_data.json', 'r') as file:
    littlemartians_data = json.load(file)