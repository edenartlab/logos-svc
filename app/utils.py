import re
import traceback

from fastapi import HTTPException


def clean_text(text):
    pattern = r"^\d+[\.:]\s*\"?"
    cleaned_text = re.sub(pattern, "", text, flags=re.MULTILINE)
    return cleaned_text


def remove_a_key(d, remove_key):
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == remove_key:
                del d[key]
            else:
                remove_a_key(d[key], remove_key)


def handle_error(e):
    error_detail = {
        "error_type": type(e).__name__,
        "error_message": str(e),
        "traceback": traceback.format_exc(),
    }
    raise HTTPException(status_code=400, detail=error_detail)
