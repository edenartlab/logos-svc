from typing import Optional
from PIL import Image, ImageDraw

from ..plugins import replicate, elevenlabs, s3
from ..character import Character
from ..utils import combine_speech_video, wrap_text, get_font, create_dynamic_model
from ..scenarios.tasks import general_assistant
from ..models.tasks import SimpleAssistantRequest
from ..plugins import elevenlabs


def select_random_voice(character: Character = None):
    if not character:
        return elevenlabs.get_random_voice()

    gender_schema = create_dynamic_model("gender", ["male", "female"])

    prompt = f"What is the most likely gender of the following character, male or female?\n\nName: {character.name}\n\nDescription: {character.identity}"

    request = SimpleAssistantRequest(
        prompt=prompt,
        model="gpt-3.5-turbo",
        params={"temperature": 0.0, "max_tokens": 10},
        output_schema=gender_schema
    )

    try:
        gender = general_assistant(request)
        voice_id = elevenlabs.get_random_voice(gender=gender)
    except Exception as e:
        voice_id = elevenlabs.get_random_voice()
    finally:
        return voice_id


def talking_head(
    character: Character,
    text: str, 
    width: Optional[int] = None,
    height: Optional[int] = None,
    gfpgan: bool = False,
    gfpgan_upscale: int = 1
) -> str:
    if character.voice:
        voice_id = character.voice
    else:
        voice_id = select_random_voice(character)
    
    audio_bytes = elevenlabs.tts(
        text, 
        voice=voice_id
    )

    audio_url = s3.upload(audio_bytes, "mp3")
    output_url, thumbnail_url = replicate.wav2lip(
        face_url=character.image,
        speech_url=audio_url,
        gfpgan=gfpgan,
        gfpgan_upscale=gfpgan_upscale,
        width=width,
        height=height,
    )
    return output_url, thumbnail_url


def screenplay_clip(
    character: Optional[Character],
    speech: str,
    image_text: str,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    if not character:
        voice_id = select_random_voice()
    else:
        if character.voice:
            voice_id = character.voice
        else:
            voice_id = select_random_voice(character)
    audio_bytes = elevenlabs.tts(
        speech, 
        voice=voice_id
    )
    audio_url = s3.upload(audio_bytes, "mp3")
    video_url, thumbnail_url = replicate.txt2vid(
        interpolation_texts=[image_text],
        width=width,
        height=height,
    )
    output_filename = combine_speech_video(audio_url, video_url)
    return output_filename, thumbnail_url


def comic_strip(
    images: list[Image.Image],
    captions: list[str],
    margin: int = 30,
    padding: int = 25,
    caption_padding_top: int = 10,
    line_spacing: int = 1.3,
    font_size: int = 48,
    font_ttf: str = 'Raleway-Light.ttf'
):
    font = get_font(font_ttf, font_size)
    num_panels = len(images)
    caption_box_height = 3 * int(1.5 * font.size)

    width, height = 1024, 1024 #images[0].size
    total_width = width * 2 + margin
    total_height = height * 2 + caption_box_height * 2 + margin

    composite_image = Image.new('RGB', (total_width, total_height), color='white')

    draw = ImageDraw.Draw(composite_image)
    draw.rectangle([(0, 0), (total_width, total_height)], fill='black')

    caption_box_height = 3 * int(1.5 * font.size) + 2 * caption_padding_top

    for i, image in enumerate(images):

        if num_panels == 3 and i == 0:
            x = 0
            y = 0
            new_height = height * 2 + caption_box_height * 2 + margin
            new_width = width
        else:
            if num_panels == 3:
                x = width + margin
                y = ((i - 1) * (height + caption_box_height + margin)) if i == 1 else ((i - 1) * (height + caption_box_height))
                new_height = height
                new_width = width
            else:
                x = (i % 2) * (width + margin) if i % 2 == 0 else (i % 2) * width + margin
                y = (i // 2) * (height + caption_box_height) if i // 2 == 0 else (i // 2) * (height + caption_box_height + margin)
                new_height = height
                new_width = width

        resized_image = image.resize((new_width, new_height))

        composite_image.paste(resized_image, (x, y))

        caption_box = Image.new('RGB', (new_width, caption_box_height), color='black')
        draw = ImageDraw.Draw(caption_box)

        wrapped_caption = wrap_text(draw, captions[i], font, new_width - 2 * padding)
        caption_y = caption_padding_top
        for line in wrapped_caption:
            draw.text((padding, caption_y), line, fill='white', font=font)
            caption_y += int(line_spacing * font.size)

        composite_image.paste(caption_box, (x, y + new_height))

        if (num_panels == 4 and i == 0) or (num_panels == 3 and i == 1):
            thumbnail = Image.new('RGB', (new_width, new_height + caption_box_height), color='white')
            thumbnail.paste(resized_image, (0, 0))
            thumbnail.paste(caption_box, (0, new_height))

    return composite_image, thumbnail


def poster(
    image: Image.Image,
    caption: str,
    margin: int = 32,
    caption_padding_top: int = 10,
    line_spacing: int = 1.3,
    font_size: int = 36,
    font_ttf: str = 'Raleway-Light.ttf',
    shadow_offset: tuple = (1, 1.4),
    font_color: str = '#e7e7e7',
    shadow_color: str = '#d3d3d3'
):
    font = get_font(font_ttf, font_size)
    width, height = image.size

    draw = ImageDraw.Draw(Image.new('RGB', (width, height)))
    wrapped_caption = wrap_text(draw, caption, font, width - 2 * margin)
    num_lines = len(wrapped_caption)

    caption_box_height = num_lines * int(line_spacing * font.size) + 2 * caption_padding_top

    total_width = width + margin
    total_height = height + caption_box_height + margin

    composite_image = Image.new('RGB', (total_width, total_height), color='white')

    draw = ImageDraw.Draw(composite_image)
    draw.rectangle([(0, 0), (total_width, total_height)], fill='black')

    resized_image = image.resize((width, height))

    composite_image.paste(resized_image, (int(margin/2), int(margin/2)))

    caption_box = Image.new('RGB', (width, caption_box_height), color='black')
    draw = ImageDraw.Draw(caption_box)

    caption_y = caption_padding_top + 0*margin/2
    for line in wrapped_caption:
        draw.text((margin + shadow_offset[0], caption_y + shadow_offset[1]), line, fill=shadow_color, font=font)
        draw.text((margin, caption_y), line, fill=font_color, font=font)
        caption_y += int(line_spacing * font.size)

    composite_image.paste(caption_box, (0, height))

    thumbnail = Image.new('RGB', (width, height + caption_box_height), color='white')

    thumbnail.paste(resized_image, (0, 0))
    thumbnail.paste(caption_box, (0, height))

    return composite_image, thumbnail