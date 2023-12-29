from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
import logging
from .routers import scenario, chat, story, dags

app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"An error occurred: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=400,
        content={"message": f"An error occurred: {exc}"},
    )


app.include_router(scenario.router)
app.include_router(chat.router)
app.include_router(story.router)
app.include_router(dags.router)


@app.get("/")
async def main():
    return {"status": "running"}
