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


# def kojii_untitledxyz(request: KojiiUntitledxyzRequest, callback=None):
#     import requests
#     from ..creation_interfaces import KojiiUntitledxyzRequest
#     for h in [0.0, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.333333, 0.4, 0.45, 0.5, 0.55, 0.6, 0.666667, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99, 1.0]:
#         for s in [Type.column]: #, Type.context]:
#             req = KojiiUntitledxyzRequest(
#                 human_machine_nature=h,
#                 type=s,
#                 seed=5
#             )
#             image_url, thumbnail_url, config = kojii_untitledxyz1(req)
#             print("\n\n\n\n\n\n\n\n\n================")
#             print("DO ", s, h)
#             print(f'images/bbb_{s.value}_{h}.jpg')
#             with open(f'images/bbb_{s.value}_{h}.jpg', 'wb') as f:
#                 f.write(requests.get(image_url).content)


def kojii_untitledxyz(request: KojiiUntitledxyzRequest, callback=None):
    seed = request.seed if request.seed else random.randint(0, 1000000)

    print("====== UNTITLED =======")
    print(request)

    if request.type == Type.column:

        if request.human_machine_nature < 1 / 3:
            text_inputs_to_interpolate = [
                "close up of a single column, highly detailed, pen and ink, stone drawn with light yellow, orange, light brown, solid white background, sharpness, noise.",
                "close up of a single column fragment, dense wires and thick electrical cables, computer circuits, corrosion, pen and ink, wires drawn with pale yellow, red, blue, green, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 3 * request.human_machine_nature,
                3 * request.human_machine_nature,
            ]

        elif request.human_machine_nature < 2 / 3:
            text_inputs_to_interpolate = [
                "close up of a single column fragment, dense wires and thick electrical cables, computer circuits, corrosion, pen and ink, wires drawn with pale yellow, red, blue, green, solid white background, sharpness, noise.",
                "close up of a single column fragment, pen and ink, dense vegetation, wrapped in vines emerging from cracks, large leaves, dense lichen, diverse plants drawn with bright green, red, orange, blue, cyan, magenta, yellow, oversaturated, neons, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 3 * (request.human_machine_nature - 1 / 3),
                3 * (request.human_machine_nature - 1 / 3),
            ]

        else:
            text_inputs_to_interpolate = [
                "close up of a single column fragment, pen and ink, dense vegetation, wrapped in vines emerging from cracks, large leaves, dense lichen, diverse plants drawn with bright green, red, orange, blue, cyan, magenta, yellow, oversaturated, neons, solid white background, sharpness, noise.",
                "close up of a single column, highly detailed, pen and ink, stone drawn with light yellow, orange, light brown, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 3 * (request.human_machine_nature - 2 / 3),
                3 * (request.human_machine_nature - 2 / 3),
            ]

    elif request.type == Type.context:

        if request.human_machine_nature < 1 / 3:
            text_inputs_to_interpolate = [
                "isometric architectural drawing, displaying an ultra close up of distorted roman columns connected to a modern building, emphasizing stone corinthian capitals and white blocks, pen and ink, yellow, orange, light brown, solid white background, sharpness, noise",
                "architectural drawing, giant blocks, displaying an ultra close up of a modernist building made of computer parts, emphasizing entangled wires with intense precision, the intricate web of wires are seen up close, accentuating the fusion of modern and ancient, the image depicts wires illustrated with vibrant colors, solid color background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 3 * request.human_machine_nature,
                3 * request.human_machine_nature,
            ]

        elif request.human_machine_nature < 2 / 3:
            text_inputs_to_interpolate = [
                "architectural drawing, giant blocks, displaying an ultra close up of a modernist building made of computer parts, emphasizing entangled wires with intense precision, the intricate web of wires are seen up close, accentuating the fusion of modern and ancient, the image depicts wires illustrated with vibrant colors, solid color background, sharpness, noise.",
                "an isometric architectural drawing, displaying an ultra close up of a modern superstructure, geometric stone blocks, emphasis on dense overwhelming vines with intense precision, plants are shot up close, accentuating the fusion of nature and columns, the image depicts giant leaves illustrated with vibrant colors, solid white background, sharpness, noise.",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 3 * (request.human_machine_nature - 1 / 3),
                3 * (request.human_machine_nature - 1 / 3),
            ]

        else:
            text_inputs_to_interpolate = [
                "an isometric architectural drawing, displaying an ultra close up of a modern superstructure, geometric stone blocks, emphasis on dense overwhelming vines with intense precision, plants are shot up close, accentuating the fusion of nature and columns, the image depicts giant leaves illustrated with vibrant colors, solid white background, sharpness, noise.",
                "isometric architectural drawing, displaying an ultra close up of distorted roman columns connected to a modern building, emphasizing stone corinthian capitals and white blocks, pen and ink, yellow, orange, light brown, solid white background, sharpness, noise",
            ]
            text_inputs_to_interpolate_weights = [
                1 - 3 * (request.human_machine_nature - 2 / 3),
                3 * (request.human_machine_nature - 2 / 3),
            ]

    config = {
        "mode": "create",
        "text_input": " to ".join(text_inputs_to_interpolate),
        "text_inputs_to_interpolate": "|".join(text_inputs_to_interpolate),
        "text_inputs_to_interpolate_weights": "|".join(
            [str(t) for t in text_inputs_to_interpolate_weights],
        ),
        "lora_scale": 0.8,
        "seed": seed,
        "guidance_scale": 8.0,
    }

    print("CONFIG")
    print(request.human_machine_nature)
    print(config["text_inputs_to_interpolate"])
    print(config["text_inputs_to_interpolate_weights"])
    print("=======\n\n\n")

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url
