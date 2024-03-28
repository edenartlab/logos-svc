import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class Type(Enum):
    column = "column"
    context = "context"


class KojiiUntitledxyzRequest(BaseModel):
    """
    A request for Untitledxyz endpoint
    """

    type: Type = Field(default=Type.column, description="Column or Context")
    human_machine_nature: float = Field(
        default=0.5,
        description="Human (0) vs machine (0.5) vs nature (1)",
        ge=0.0,
        le=1.0,
    )
    seed: Optional[int] = Field(default=None, description="Random seed")


def kojii_untitledxyz(request: KojiiUntitledxyzRequest, callback=None):
    seed = request.seed if request.seed else random.randint(0, 1000000)

    print("====== UNTITLED =======")
    print(request)

    if request.type == Type.column:

        if request.human_machine_nature < 0.5:
            text_inputs_to_interpolate = [
                "close up of a single column, highly detailed, pen and ink, stone drawn with light yellow, orange, light brown, solid white background, sharpness, noise.",
                "close up of a single column fragment, dense wires and thick electrical cables, computer circuits, corrosion, pen and ink, wires drawn with pale yellow, red, blue, green, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 2 * request.human_machine_nature,
                2 * request.human_machine_nature,
            ]

        else:
            text_inputs_to_interpolate = [
                "close up of a single column fragment, dense wires and thick electrical cables, computer circuits, corrosion, pen and ink, wires drawn with pale yellow, red, blue, green, solid white background, sharpness, noise.",
                "close up of a single column fragment, pen and ink, dense vegetation, wrapped in vines emerging from cracks, large leaves, dense lichen, diverse plants drawn with bright green, red, orange, blue, cyan, magenta, yellow, oversaturated, neons, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 2 * (request.human_machine_nature - 0.5),
                2 * (request.human_machine_nature - 0.5),
            ]

    elif request.type == Type.context:

        if request.human_machine_nature < 0.5:
            text_inputs_to_interpolate = [
                "isometric architectural drawing, displaying an ultra close up of distorted roman columns connected to a modern building, emphasizing stone corinthian capitals and white blocks, pen and ink, yellow, orange, light brown, solid white background, sharpness, noise",
                "an isometric architectural drawing, displaying an ultra close up of a modernist building made of computer parts, dodecahedrons, textural details, emphasizing entangled wires with intense precision, the intricate web of wires are seen up close, accentuating the fusion of modern and ancient, the image depicts wires illustrated with vibrant colors, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 2 * request.human_machine_nature,
                2 * request.human_machine_nature,
            ]

        else:
            text_inputs_to_interpolate = [
                "an isometric architectural drawing, displaying an ultra close up of a modernist building made of computer parts, dodecahedrons, textural details, emphasizing entangled wires with intense precision, the intricate web of wires are seen up close, accentuating the fusion of modern and ancient, the image depicts wires illustrated with vibrant colors, sharpness, noise.",
                "an isometric architectural drawing, displaying an ultra close up of a modern superstructure, geometric stone blocks, emphasis on dense overwhelming vines with intense precision, plants are shot up close, accentuating the fusion of nature and columns, the image depicts giant leaves illustrated with vibrant colors, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 2 * (request.human_machine_nature - 0.5),
                2 * (request.human_machine_nature - 0.5),
            ]

    config = {
        "mode": "create",
        "text_input": " to ".join(text_inputs_to_interpolate),
        "text_inputs_to_interpolate": "|".join(text_inputs_to_interpolate),
        "text_inputs_to_interpolate_weights": "|".join(
            [str(t) for t in text_inputs_to_interpolate_weights],
        ),
        "lora": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/d2e6d1f8ccfca428ba42fa56a0384a4261d32bf1ee8b0dc952d99da9011daf39.tar",
        "lora_scale": 0.8,
        "seed": seed,
    }

    print("CONFIG")
    print(config)
    print("=======")

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url
