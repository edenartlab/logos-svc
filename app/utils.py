import re
import traceback
import requests
import math
import tempfile
import subprocess
from PIL import Image
from io import BytesIO
from fastapi import HTTPException


def handle_error(e):
    error_detail = {
        "error_type": type(e).__name__,
        "error_message": str(e),
        "traceback": traceback.format_exc(),
    }
    raise HTTPException(status_code=400, detail=error_detail)


def clean_text(text):
    pattern = r"^\d+[\.:]\s*\"?"
    cleaned_text = re.sub(pattern, "", text, flags=re.MULTILINE)
    return cleaned_text


def text_to_lines(text):
    lines = [line for line in text.split("\n") if line]
    lines = [clean_text(line) for line in lines]
    return lines


def remove_a_key(d, remove_key):
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == remove_key:
                del d[key]
            else:
                remove_a_key(d[key], remove_key)


def download_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image
    

def calculate_target_dimensions(images, max_pixels):
    min_w = float('inf')
    min_h = float('inf')

    total_aspect_ratio = 0.0

    for image_url in images:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        width, height = image.size
        min_w = min(min_w, width)
        min_h = min(min_h, height)
        total_aspect_ratio += width / height

    avg_aspect_ratio = total_aspect_ratio / len(images)

    if min_w / min_h > avg_aspect_ratio:
        target_height = min_h
        target_width = round(target_height * avg_aspect_ratio)
    else:
        target_width = min_w
        target_height = round(target_width / avg_aspect_ratio)
    
    if target_width * target_height > max_pixels:
        ratio = (target_width * target_height) / max_pixels
        ratio = math.sqrt((target_width * target_height) / max_pixels)
        target_width = round(target_width / ratio)
        target_height = round(target_height / ratio)

    target_width -= target_width % 2
    target_height -= target_height % 2
    
    return target_width, target_height


def resize_and_crop(image, width, height):
    target_ratio = width / height
    orig_width, orig_height = image.size
    orig_ratio = orig_width / orig_height

    if orig_ratio > target_ratio:
        new_width = int(target_ratio * orig_height)
        left = (orig_width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = orig_height
    else:
        new_height = int(orig_width / target_ratio)
        top = (orig_height - new_height) // 2
        left = 0
        bottom = top + new_height
        right = orig_width

    image = image.crop((left, top, right, bottom))
    image = image.resize((width, height), Image.LANCZOS)

    return image


def create_dialogue_thumbnail(image1_url, image2_url, width, height, ext="WEBP"):
    image1 = download_image(image1_url)
    image2 = download_image(image2_url)

    half_width = width // 2

    image1 = resize_and_crop(image1, half_width, height)
    image2 = resize_and_crop(image2, half_width, height)

    combined_image = Image.new('RGB', (width, height))

    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (half_width, 0))

    img_byte_arr = BytesIO()
    combined_image.save(img_byte_arr, format=ext)
    
    return img_byte_arr.getvalue()


def concatenate_videos(video_files, output_file):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
        for video_file in video_files:
            f.write(f"file '{video_file}'\n")
        f.flush()        
        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", f.name, "-c", "copy", output_file])
