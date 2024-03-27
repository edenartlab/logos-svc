import os
import requests
import tempfile

from .. import utils
from ..plugins import replicate, s3
from ..character import EdenCharacter
from ..llm import LLM
from ..models import ComicRequest, ComicResult
from ..prompt_templates.comic import comicwriter_system_template
from .animation import comic_strip


def illustrated_comic(request: ComicRequest):
    params = {"temperature": 1.0, "max_tokens": 2000, **request.params}
    loras = {
        "Verdelis": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/f290723c93715a8eb14e589ca1eec211e10691f683d53cde37139bc7d3a91c22.tar",
    }

    comicwriter = LLM(
        model=request.model,
        system_message=comicwriter_system_template.template,
        params=params,
    )

    comic_book = comicwriter(request.prompt, output_schema=ComicResult)

    def run_panel(panel, idx):
        # pick lora of character
        # pick init image character x genre

        return replicate.sdxl(
            {
                "text_input": panel["image"],
                "lora": loras["Verdelis"],
                "width": 512 if idx == 0 else 1024,
                "height": 1024,
                "n_samples": 1,
            },
        )

    results = utils.process_in_parallel(comic_book["panels"], run_panel, max_workers=4)

    image_urls = [image_url for image_url, thumbnail in results]
    images = [utils.download_image(url) for url in image_urls]
    captions = [panel["caption"] for panel in comic_book["panels"]]

    composite_image, thumbnail_image = comic_strip(images, captions)

    img_bytes = utils.PIL_to_bytes(composite_image, ext="JPEG")
    thumbnail_bytes = utils.PIL_to_bytes(thumbnail_image, ext="WEBP")

    output_url = s3.upload(img_bytes, "jpg")
    thumbnail_url = s3.upload(thumbnail_bytes, "webp")

    return output_url, thumbnail_url
