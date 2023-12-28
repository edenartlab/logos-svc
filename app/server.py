from fastapi import FastAPI
from .routers import (
    scenario, 
    chat, 
    story, 
    dags
)

app = FastAPI()

app.include_router(scenario.router)
app.include_router(chat.router)
app.include_router(story.router)
app.include_router(dags.router)


@app.get("/")
async def main():
    return {"status": "running"}
