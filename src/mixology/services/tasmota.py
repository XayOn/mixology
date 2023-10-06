import asyncio
import logging

from aiomqtt import Client
from fastapi import Depends

from mixology.auth import auth
from mixology.database import Mongo
from mixology.models import Client as MixologyClient
from mixology.models import Tasmota
from mixology.preparer.models import Ingredient
from mixology.settings import Settings


class AnonymousTasmotaBBDDService:
    """Tasmota database service with motor."""

    def __call__(self):
        return self

    async def get_tasmotas(self, key: str, token: str):
        client = await Mongo.db.clients.find_one({"key": key, "token": token})
        if not client:
            return []
        tasmotas: list[dict[str, str]] = client["tasmotas"]
        return [Tasmota(**a) for a in tasmotas]  # type: ignore


class TasmotaBBDDService(AnonymousTasmotaBBDDService):
    """Tasmota database service with motor."""

    def __init__(self):
        super().__init__()
        self.user = None

    def __call__(self, user: MixologyClient = Depends(auth)):
        self.user = user
        return self

    async def get_tasmotas(self) -> list[Tasmota]:
        """Get tasmotas."""
        if not self.user:
            msg = "User not logged in"
            raise RuntimeError(msg)
        return await super().get_tasmotas(
            key=self.user.key,
            token=self.user.token,
        )


class TasmotaDispenserService:
    def __init__(
        self,
        tasmota_service: TasmotaBBDDService | None = None,
    ):
        self.tasmota_service = tasmota_service
        self.url = None

    def __call__(
        self,
        tasmota_service: TasmotaBBDDService = Depends(TasmotaBBDDService()),
        user: MixologyClient = Depends(auth),
    ) -> "TasmotaDispenserService":
        self.tasmota_service = tasmota_service
        self.host = Settings.mqtt_host
        self.port = Settings.mqtt_port
        self.user = user
        return self

    async def get_topic(self, tasmotas, tap_number: int) -> str:
        """Get topic from tap number.

        Tap number will be tasmota_position * tap_number
        So we need to divide it by tasmota numbers, and get the remainder

        Args:

            tap_number: Tap number in absolute position.

        Returns: Topic to publish to
        """

        # f"cmnd/{self.user.key}_"
        # tasmotas actually have 7 relays, but they start count on 1
        # so it should end up in 8... except we don't use the eighth
        return f"cmnd/{tasmotas[tap_number // 7]}/Power{ tap_number % 7}"

    async def dispense(
        self,
        ingredients: list[Ingredient],
    ) -> list[dict[str, bool]]:
        if not self.host or not self.port:
            msg = "No host/port set for TasmotaDispenserService"
            raise ValueError(msg)

        if not self.tasmota_service:
            msg = "No tasmota services found."
            raise ValueError(msg)

        tasmotas = [k.name for k in await self.tasmota_service.get_tasmotas()]

        async with Client(
            self.host,
            port=self.port,
            username=self.user.key,
            password=self.user.token,
        ) as client:
            return await asyncio.gather(
                *(
                    self._dispense(tasmotas, client, ingredient)
                    for ingredient in ingredients
                )
            )

    async def _dispense(self, tasmotas, client, ingredient: Ingredient) -> dict:
        """Dispense an ingredient."""
        topic = await self.get_topic(tasmotas, ingredient.tap_number)
        await client.publish(topic, payload=b"1")
        # Roughly estimate on how much it takes to fill 1ml...
        # this lacks precission but for now it'll be enough
        modifier = 0.4
        time_ = ingredient.amount * modifier * ingredient.density
        logging.info("Waiting %s seconds", time_)
        await asyncio.sleep(time_)
        await client.publish(topic, payload=b"0")
        return {"status": True}
