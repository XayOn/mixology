"""Simple static token-based authentication."""

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from mixology.database import Mongo
from mixology.models import Client

api_token = APIKeyHeader(name="X-API-Token")


async def auth(
    key: str,
    x_token: str = Security(api_token),
):
    """From now, just key+token simple authentication will be performed."""
    client_data = await Mongo.db.clients.find_one(
        {"key": key, "token": x_token}
    )
    if not client_data:
        raise HTTPException(status_code=400, detail="Invalid authentication")
    return Client(**client_data)
