from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
import traceback
import logging

from .scenarios import (
    monologue, 
    dialogue, 
    story, 
    chat, 
    livecode,
    tasks,
)
from .animations import (
    animated_monologue, 
    animated_dialogue, 
    animated_story,
    animated_reel,
    illustrated_comic,
    little_martian_poster,
)
from .creation_interfaces import (
    kojii_makeitrad, 
    kojii_chebel,
    kojii_untitledxyz, 
    kojii_violetforest, 
    kojii_huemin,
)
from .generator import generate_task


app = FastAPI()
router = APIRouter()

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    logging.error(f"Error: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=400,
        content={"message": f"Error: {exc}"},
    )

# Scenarios
router.add_api_route(path="/scenarios/monologue", endpoint=monologue, methods=["POST"])
router.add_api_route(path="/scenarios/dialogue", endpoint=dialogue, methods=["POST"])
router.add_api_route(path="/scenarios/story", endpoint=story, methods=["POST"])

# Animations/DAGs
router.add_api_route(path="/animation/monologue", endpoint=animated_monologue, methods=["POST"])
router.add_api_route(path="/animation/dialogue", endpoint=animated_dialogue, methods=["POST"])
router.add_api_route(path="/animation/story", endpoint=animated_story, methods=["POST"])
router.add_api_route(path="/animation/reel", endpoint=animated_reel, methods=["POST"])
router.add_api_route(path="/animation/comic", endpoint=illustrated_comic, methods=["POST"])

router.add_api_route(path="/kojii/makeitrad", endpoint=kojii_makeitrad, methods=["POST"])
router.add_api_route(path="/kojii/va2rosa", endpoint=little_martian_poster, methods=["POST"])
router.add_api_route(path="/kojii/chebel", endpoint=kojii_chebel, methods=["POST"])
router.add_api_route(path="/kojii/untitledxyz", endpoint=kojii_untitledxyz, methods=["POST"])
router.add_api_route(path="/kojii/violetforest", endpoint=kojii_violetforest, methods=["POST"])
router.add_api_route(path="/kojii/huemin", endpoint=kojii_huemin, methods=["POST"])

# Chat
router.add_api_route(path="/chat/test", endpoint=chat.test, methods=["POST"])
router.add_api_route(path="/chat/speak", endpoint=chat.speak, methods=["POST"])
router.add_api_route(path="/chat/think", endpoint=chat.think, methods=["POST"])

# LiveCoder
router.add_api_route(path="/livecode/code", endpoint=livecode.code, methods=["POST"])

# Generator
router.add_api_route(path="/tasks/create", endpoint=generate_task, methods=["POST"])

# Tasks
router.add_api_route(path="/tasks/summary", endpoint=tasks.summary, methods=["POST"])
router.add_api_route(path="/tasks/moderation", endpoint=tasks.moderation, methods=["POST"])


app.include_router(router)

@app.get("/")
def main():
    return {"status": "running"}

