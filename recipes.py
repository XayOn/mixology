import json
import asyncio
import configparser
from functools import lru_cache
from itertools import combinations
from typing import List
from fastapi import FastAPI, Query, Request
import httpx

app = FastAPI()
CONFIG = configparser.ConfigParser()
CONFIG.read('main.ini')
DISPENSERS = {}


class Dispenser:
    """Alcohol dispenser.

    Must have tasmota, and a relay configured with a peristaltic pump

    Arguments:

        url: Tasmota base url (http://192.168.1.130:8080/)
        sensor_no: Sensor number (1)
        time_per_cl: Measure how much time it takes for your pump to pump a cl
    """
    def __init__(self, url: str, sensor_no: int, time_per_cl: int):
        self.time_per_half_cl = time_per_cl / 2
        self.url = f"{url}?m=1&o={sensor_no}"

    async def dispense(self, quantity):
        async with httpx.AsyncClient() as client:
            res1 = await client.get(self.url)
            await asyncio.sleep(self.time_per_half_cl * (quantity / 2))
            res2 = await client.get(self.url)
            return [res1, res2]


for section in CONFIG.sections():
    config = CONFIG[section]
    DISPENSERS[section] = Dispenser(config.get('url'),
                                    config.getint('sensor_no'),
                                    config.getint('time_per_cl'))


class Cocktail(dict):
    """Represent a cocktail"""
    def __hash__(self):
        return self['id']

    @property
    def alcohols(self) -> set:
        """Return list of alcohols in ingredients"""
        def is_juice(ing):
            """Avoid non-alcoholic drinks"""
            fsc = ('bitter', 'juice', 'syrup', 'spoon', 'cola', 'water')
            return any(a in ing.lower() for a in fsc)

        return set(
            filter(lambda x: x,
                   [a if not is_juice(a) else None for a in self.ingredients]))

    @property
    def ingredients(self):
        """non-special ingredients, may return '' on special ones."""
        return [a.get('ingredient', '') for a in self['ingredients']]

    def quantity(self, ingredient_name):
        match = next(
            iter([
                ing for ing in self.ingredients
                if ing.get('ingredient') == ingredient_name
            ]))
        return match['amount']

    @property
    def all_ingredients(self):
        """All ingredients, including special ones"""
        return ', '.join([
            (f"{a.get('ingredient', a.get('special'))} {a.get('amount', '')}"
             f" {a.get('unit', '')}") for a in self['ingredients']
        ])

    def num_similar(self, other):
        """Return the number of equal alcohols in both beverages"""
        return len(self.alcohols & other.alcohols)

    def __repr__(self):
        return f"""{self['name']}
================

Ingredients: {self.all_ingredients}
Preparation: {self.get('preparation', '')}
Glass: {self.get('glass', 'Generic')}
Garnish: {self.get('garnish', 'None')}\n\n"""


@lru_cache
def sorted_recipes(curr):
    """Sort recipes.

    Given a set of base ingredients, get the most recipes we can achieve by
    buying the less ingredients
    """
    curr = set(curr)
    cocktails = [
        Cocktail(b | dict(id=a))
        for a, b in enumerate(json.load(open('recipes.json')))
    ]
    similarity = {}
    for p1, p2 in combinations(cocktails, 2):
        similarity.setdefault((p1, p2), p1.num_similar(p2))
    similarity = sorted(similarity, key=lambda x: similarity[x], reverse=True)
    sorted_ids = []
    for (left, right) in similarity:
        if left not in sorted_ids:
            sorted_ids.append(left)
        elif right not in sorted_ids:
            sorted_ids.append(right)

    return [a for a in sorted_ids if not a.alcohols - curr]


async def dispense(alcohol, quantity):
    if dispenser := DISPENSERS.get(alcohol):
        await dispenser.dispense(quantity)
    else:
        return None


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.get("/recipes/")
async def calculate_recipes(current: List[str] = Query(None)):
    # I have: "Vodka", "Gin", "Tequila", "White Rum", "Triple Sec", "Vermouth"
    return sorted_recipes(tuple(current))


@app.post("/recipes/")
async def do_recipe(request: Request):
    cocktail = Cocktail(await request.json())
    result = await asyncio.gather(
        *[dispense(a, cocktail.quantity(a)) for a in cocktail.alcohols])
    return result
