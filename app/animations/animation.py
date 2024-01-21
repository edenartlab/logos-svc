from typing import Optional
from PIL import Image, ImageDraw

from ..plugins import replicate, elevenlabs, s3
from ..character import EdenCharacter
from ..utils import combine_speech_video, wrap_text, get_font


def talking_head(
    character: EdenCharacter,
    text: str, 
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    audio_bytes = elevenlabs.tts(
        text, 
        voice=character.voice
    )
    audio_url = s3.upload(audio_bytes, "mp3")
    output_url, thumbnail_url = replicate.wav2lip(
        face_url=character.image,
        speech_url=audio_url,
        gfpgan=False,
        gfpgan_upscale=1,
        width=width,
        height=height,
    )
    return output_url, thumbnail_url


def screenplay_clip(
    character: EdenCharacter,
    speech: str,
    image_text: str,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    audio_bytes = elevenlabs.tts(
        speech, 
        voice=character.voice
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
    font_ttf: str = 'Roboto-Regular.ttf'
):
    font = get_font(font_ttf, font_size)
    caption_box_height = 3 * int(1.5 * font.size)

    width, height = images[0].size
    total_width = width * 2 + margin
    total_height = height * 2 + caption_box_height * 2 + margin

    composite_image = Image.new('RGB', (total_width, total_height), color='white')

    draw = ImageDraw.Draw(composite_image)
    draw.rectangle([(0, 0), (total_width, total_height)], fill='black')

    caption_box_height = 3 * int(1.5 * font.size) + 2 * caption_padding_top

    first_pane_image = None

    for i, image in enumerate(images):

        x = (i % 2) * (width + margin) if i % 2 == 0 else (i % 2) * width + margin
        y = (i // 2) * (height + caption_box_height) if i // 2 == 0 else (i // 2) * (height + caption_box_height + margin)

        composite_image.paste(image, (x, y))

        caption_box = Image.new('RGB', (width, caption_box_height), color='black')
        draw = ImageDraw.Draw(caption_box)

        wrapped_caption = wrap_text(draw, captions[i], font, width - 2 * padding)
        caption_y = caption_padding_top
        for line in wrapped_caption:
            draw.text((padding, caption_y), line, fill='white', font=font)
            caption_y += int(line_spacing * font.size)

        composite_image.paste(caption_box, (x, y + height))

        if i == 0:
            thumbnail = Image.new('RGB', (width, height + caption_box_height), color='white')
            thumbnail.paste(image, (0, 0))
            thumbnail.paste(caption_box, (0, height))

    return composite_image, thumbnail