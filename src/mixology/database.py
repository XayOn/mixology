from typing import ClassVar

import motor.motor_asyncio
from redis import asyncio as aioredis


class Mongo:
    db: ClassVar[motor.motor_asyncio.AsyncIOMotorDatabase]


class Redis:
    db: ClassVar[aioredis.Redis]
