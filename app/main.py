from fastapi import FastAPI
from .routers import scenario#, another  # Import routers from the routers module

app = FastAPI()

# Include routers from the routers package
app.include_router(scenario.router)
#app.include_router(another.router)

# Define a simple route for the root of the service
@app.get("/")
async def read_root():
    return {"msg": "Hello, World"}

# You can add additional routes here or in separate modules within the routers package.
