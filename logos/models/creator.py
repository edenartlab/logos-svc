from enum import Enum
from typing import List, Optional
from pydantic import Field, BaseModel, ValidationError


class Thought(BaseModel):
    """
    Probability percentage that the character responds to the conversation
    """

    probability: str = Field(
        description="A percentage chance that the character will respond to the conversation",
    )


class GeneratorMode(Enum):
    create = "create"
    controlnet = "controlnet"
    remix = "remix"
    blend = "blend"
    upscale = "upscale"
    interpolate = "interpolate"
    real2real = "real2real"
    txt2vid = "txt2vid"
    img2vid = "img2vid"
    vid2vid = "vid2vid"


class Config(BaseModel):
    """
    JSON config for Eden generator request
    """

    generator: GeneratorMode = Field(description="Which generator to use")
    text_input: Optional[str] = Field(description="Text prompt that describes image")
    seed: Optional[int] = Field(description="Seed for random number generator")
    init_image: Optional[str] = Field(
        description="Path to image file for create, remix, upscale, controlnet, img2vid, or vid2vid",
    )
    init_video: Optional[str] = Field(description="Path to video file for vid2vid")
    init_image_strength: Optional[float] = Field(
        description="Strength of init image, default 0.15",
    )
    control_image: Optional[str] = Field(
        description="Path to image file for controlnet",
    )
    control_image_strength: Optional[float] = Field(
        description="Strength of control image for controlnet, default 0.6",
    )
    interpolation_init_images: Optional[List[str]] = Field(
        description="List of paths to image files for real2real or blend",
    )
    interpolation_texts: Optional[List[str]] = Field(
        description="List of text prompts for interpolate",
    )
    interpolation_seeds: Optional[List[int]] = Field(
        description="List of seeds for interpolation texts",
    )
    n_frames: Optional[int] = Field(description="Number of frames in output video")


class StoryNamedCharacters(BaseModel):
    """
    List of named characters in story draft
    """

    character_names: List[str] = Field(description="List of characters named by user")


class StoryConfig(BaseModel):
    """
    List of scene descriptions for Eden story request
    """

    scenes: List[str] = Field(description="List of Scenes in the story")
    characters: List[str] = Field(description="List of character names in the story")


class StoryCreatorOutput(BaseModel):
    """
    Output of creator LLM containing a JSON config and a message to the user
    """

    config: Optional[StoryConfig] = Field(description="Config for Eden generator")
    named_characters: List[str] = Field(
        description="List of characters named by the user",
    )
    message: str = Field(description="Message to user")


class CreatorOutput(BaseModel):
    """
    Output of creator LLM containing a JSON config and a message to the user
    """

    config: Config = Field(description="Config for Eden generator")
    message: str = Field(description="Message to user")


class CreatorInput(BaseModel):
    """
    Input to creator LLM containing a prompt, and optionally a list of attachments
    """

    message: str = Field(description="Message to LLM")
    attachments: Optional[List[str]] = Field(
        default_factory=list,
        description="List of file paths to attachments",
    )


class StoryCreatorOutput(BaseModel):
    """
    Output of story creator LLM containing a JSON config and a message to the user
    """

    config: StoryConfig = Field(description="Config for Eden generator")
    message: str = Field(description="Message to user")


class StoryCreatorInput(BaseModel):
    """
    Input to story creator LLM containing a prompt, and optionally a list of attachments
    """

    message: str = Field(description="Message to LLM")
    attachments: Optional[List[str]] = Field(
        default_factory=list,
        description="List of file paths to attachments",
    )
