from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel

from mixology.preparer.models import Ingredient
from mixology.services.tasmota import TasmotaDispenserService

router = APIRouter()


class Response(BaseModel):
    status: bool


@router.post("/prepare", response_model=list[Response])
async def prepare_recipe(
    ingredients: list[Ingredient],
    background_tasks: BackgroundTasks,
    dispenser_service=Depends(TasmotaDispenserService()),
):
    background_tasks.add_task(dispenser_service.dispense, ingredients)

    return [{"status": True}]
