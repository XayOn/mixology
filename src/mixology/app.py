import logging
from pathlib import Path

import motor
import motor.motor_asyncio
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from redis import asyncio as aioredis

from mixology.database import Mongo, Redis
from mixology.routes import setup_routes


def setup_bbdd():
    from mixology.settings import Settings

    db = motor.motor_asyncio.AsyncIOMotorClient(Settings.mongodb_url)

    Mongo.db = db.mixology

    redis = aioredis.from_url(Settings.redis_url)
    Redis.db = redis


def get_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_routes(app)
    setup_bbdd()

    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logging.error(f"{request} {request.body}: {exc_str}")
        content = {"status_code": 10422, "message": exc_str, "data": None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.mount(
        "/static",
        StaticFiles(directory=Path(__file__).parent / "static"),
        name="static",
    )

    return app
