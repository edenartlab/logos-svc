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
    human_machine_nature: float = Field(default=0.5, description="Human (0) vs machine (0.5) vs nature (1)", ge=0.0, le=1.0)

def kojii_untitledxyz(request: KojiiUntitledxyzRequest, callback=None):
    
    text_inputs_to_interpolate = [

    ]
    
    if request.human_machine_nature < 0.5:

        text_inputs_to_interpolate_weights = [
            2 * request.human_machine_nature
        ]

    config = {
        "mode": "create",
        "text_input": " to ".join(text_inputs_to_interpolate),
        "text_inputs_to_interpolate": "|".join(text_inputs_to_interpolate),
        "text_inputs_to_interpolate_weights": " | ".join([str(t) for t in text_inputs_to_interpolate_weights]),
        "lora": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/d2e6d1f8ccfca428ba42fa56a0384a4261d32bf1ee8b0dc952d99da9011daf39.tar",
        "lora_scale": 0.8,
    }
    

#     sudo cog predict -i mode=create -i text_inputs_to_interpolate="prompt1|prompt2" -i text_inputs_to_interpolate_weights="0.3|0.7"
# add the loraurl for this concept: https://app.eden.art/creators/untitledxyz?conceptId=65b927bcc69501b06686d68d
# the weights will be normalized to sum=1 in my code
    
    return {"hello": "world"}