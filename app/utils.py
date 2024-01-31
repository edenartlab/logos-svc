import tempfile
import time
import os
import re
import traceback
import requests
import math
import tempfile
import subprocess
import datetime
import orjson
from PIL import Image, ImageFont
from io import BytesIO
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor, as_completed



def orjson_dumps(v, *, default, **kwargs):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, **kwargs).decode()


def now_tz():
    # Need datetime w/ timezone for cleanliness
    # https://stackoverflow.com/a/24666683
    return datetime.datetime.now(datetime.timezone.utc)


def get_font(font_name, font_size):
    font_path = os.path.join(os.path.dirname(__file__), "fonts", font_name)
    font = ImageFont.truetype(font_path, font_size)
    return font


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
    

def PIL_to_bytes(image, ext="JPEG", quality=95):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format=ext, quality=quality)
    return img_byte_arr.getvalue()


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
    standard_fps = "30"  # Target frame rate

    # Step 1: Convert all videos to the same frame rate
    converted_videos = []
    for i, video in enumerate(video_files):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp:
            output_video = temp.name
            convert_command = ['ffmpeg', '-y', '-loglevel', 'panic', '-i', video, '-r', standard_fps, '-c:a', 'copy', output_video]
            subprocess.run(convert_command)
            converted_videos.append(output_video)
    
    print("videos", converted_videos)
    
    # Create the filter_complex string
    filter_complex = "".join([f"[{i}:v] [{i}:a] " for i in range(len(converted_videos))])
    filter_complex += f"concat=n={len(converted_videos)}:v=1:a=1 [v] [a]"

    # Concatenate videos
    concat_command = ['ffmpeg']
    for video in converted_videos:
        concat_command.extend(['-i', video])
    concat_command.extend(['-y', '-loglevel', 'panic','-filter_complex', filter_complex, '-map', '[v]', '-map', '[a]', output_file])
    subprocess.run(concat_command)

    # Step 4: Delete temporary files
    for video in converted_videos:
        os.remove(video)


def combine_speech_video(audio_url: str, video_url: str):
    audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=True)
    video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=True)
    output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)

    subprocess.run(['wget', '-nv', '-O', audio_file.name, audio_url])
    subprocess.run(['wget', '-nv', '-O', video_file.name, video_url])

    # get the duration of the audio file
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_file.name]
    audio_duration = subprocess.check_output(cmd).decode().strip()

    # loop the video
    looped_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=True)
    cmd = ['ffmpeg', '-y', '-loglevel', 'panic', '-stream_loop', '-1', '-i', video_file.name, '-c', 'copy', '-t', audio_duration, looped_video.name]
    subprocess.run(cmd)

    # merge the audio and the looped video
    cmd = ['ffmpeg', '-y', '-loglevel', 'panic', '-i', looped_video.name, '-i', audio_file.name, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-shortest', output_file.name]
    subprocess.run(cmd)

    return output_file.name


def exponential_backoff(
    func, 
    max_attempts=5, 
    initial_delay=1, 
):
    delay = initial_delay
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts:
                raise e
            print(f"Attempt {attempt} failed. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay = delay * 2


def process_in_parallel(
    array, 
    func, 
    max_workers=3
):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, item, index): index for index, item in enumerate(array)}
        results = [None] * len(array)
        for future in as_completed(futures):
            try:
                index = futures[future]
                results[index] = future.result()
            except Exception as e:
                print(f"Task error: {e}")
                for f in futures:
                    f.cancel()
                raise e
    return results


def handle_error(e):
    error_detail = {
        "error_type": type(e).__name__,
        "error_message": str(e),
        "traceback": traceback.format_exc(),
    }
    raise HTTPException(status_code=400, detail=error_detail)


def wrap_text(draw, text, font, max_width):
    lines = []
    words = text.split()

    while words:
        line = ''
        while words and draw.textlength(line + words[0], font=font) <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    
    return lines
