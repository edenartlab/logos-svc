from fastapi import FastAPI
from .routers import scenario, chat, story
app = FastAPI()

app.include_router(scenario.router)
app.include_router(chat.router)
app.include_router(story.router)


@app.get("/")
async def main():
    return {"status": "running"}

# monologue
# dialogue
# story w/ creations (stub)
# comic book w/ creations
# eden assistant, chat monitor