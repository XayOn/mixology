import json
import secrets
from datetime import timedelta

from mixology.database import Redis


class TemporaryTokenService:
    def __init__(self):
        self.redis = None

    def __call__(self):
        self.redis = Redis.db
        return self

    async def get_token(self, token: str) -> dict:
        """Get a temporary token to be used in the initial setup."""
        if not self.redis:
            msg = "Redis is not initialized."
            raise Exception(msg)

        if data := await self.redis.get(token):
            return json.loads(data)

        return {}

    async def set_token(self, key: str, token: str) -> str:
        """Set a temporary token to be used in the initial setup."""
        if not self.redis:
            msg = "Redis is not initialized."
            raise Exception(msg)

        temp_token = secrets.token_urlsafe(4)

        await self.redis.setex(
            temp_token,
            timedelta(minutes=5),
            json.dumps({"key": key, "token": token}),
        )

        return temp_token
