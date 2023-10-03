import asyncio
import databases
import json
from contextlib import suppress

import sqlalchemy
from asyncio_mqtt import Client
from fastapi import FastAPI

from mixology.preparer.models import Ingredient
from mixology.settings import Settings


def get_time_total(ingredient: Ingredient):
    return ingredient.amount * ingredient.density


database = databases.Database(Settings.db_uri)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


class TasmotaFinderTask:
    """Background task to update tasmota found clients."""

    def __init__(self, url: str, app: FastAPI):
        self.tasmotas = {}
        self.app = app
        self.url = url

    @property
    def tasmota_taps(self):
        return {}

    async def retry_main(self):
        while True:
            with suppress(Exception):
                await self.run_main()
                await asyncio.sleep(5)

    async def run_main(self):
        async with Client(self.url) as client:
            btop = "tasmota/discovery/+/config"
            async with client.filtered_messages(btop) as messages:
                await client.subscribe("tasmota/discovery/#")
                async for message in messages:
                    loaded = json.loads(message.payload)
                    if any(loaded["rl"]):
                        relays = [a for a, b in enumerate(loaded["rl"]) if b]
                        self.tasmotas[loaded["t"]] = relays

    async def dispense(self, client, ingredient: Ingredient):
        topic = self.tasmota_taps[ingredient.tap_number]
        await client.publish(topic, payload=b"ON")
        await asyncio.sleep(get_time_total(ingredient))
        await client.publish(topic, payload=b"OFF")
        return {"status": False}
