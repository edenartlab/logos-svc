import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from fastapi.testclient import TestClient
from app.server import app
from app import mongo
from app.character import EdenCharacter
from app.models.tasks import SimpleAssistantRequest
from app.scenarios.tasks import general_assistant
from app.utils import create_dynamic_model
from app.plugins import elevenlabs

client = TestClient(app)

# def test_func():
#     """
#     Test function
#     """

#     prompt = "What is the gender of the following name: Lisa"
#     gender = create_dynamic_model("gender", ["male", "female"])

#     request = SimpleAssistantRequest(
#         prompt=prompt,
#         model="gpt-3.5-turbo",
#         params={"temperature": 0.0, "max_tokens": 10},
#         output_schema=gender
#     )

#     result = general_assistant(request)

#     voice_id = elevenlabs.get_random_voice(result)
#     print(voice_id)


class Country(Enum):
    france = "France"
    germany = "Germany"
    switzerland = "Switzerland"
    usa = "USA"
    japanasia = "Japan Asia"


class CountrySelection(BaseModel):
    """
    Country
    """

    country: Country = Field(description="Country")


def test_func2():
    """
    Test mongo
    """

    prompt = "What country is this city in? Tokyo"
    country = create_dynamic_model(
        "country",
        ["France", "Germany", "Switzerland", "USA", "Japan Asia ok yay"],
    )

    request = SimpleAssistantRequest(
        prompt=prompt,
        model="gpt-3.5-turbo",
        params={"temperature": 0.0, "max_tokens": 10},
        output_schema=country,
    )

    result = general_assistant(request)
    print(type(result))

    print(result)
