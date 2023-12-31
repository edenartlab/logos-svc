from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import traceback
import logging
from .routers import scenario, chat, story, dags, generator, summary

app = FastAPI()

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    logging.error(f"An error occurred: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=400,
        content={"message": f"An error occurred: {exc}"},
    )

app.include_router(scenario.router)
app.include_router(chat.router)
app.include_router(story.router)
app.include_router(dags.router)
app.include_router(summary.router)
app.include_router(generator.router)

@app.get("/")
def main():
    return {"status": "running"}
