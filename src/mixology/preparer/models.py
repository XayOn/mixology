from pydantic import BaseModel


class Ingredient(BaseModel):
    tap_number: int
    density: int
    amount: int
