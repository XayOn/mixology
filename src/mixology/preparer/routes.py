from fastapi import APIRouter

from mixology.preparer.models import Ingredient

router = APIRouter()


@router.post("/prepare")
async def prepare_recipe(ingredients: list[Ingredient]):
    return ingredients
