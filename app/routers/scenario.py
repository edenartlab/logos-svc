# routers/scenario.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/scenarios/{scenario_id}")
async def read_scenario(scenario_id: int):
    return {"scenario_id": scenario_id}

# Add more scenario-related routes here
