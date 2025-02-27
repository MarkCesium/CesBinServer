from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import api_router
from src.core.config import settings
from src.core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging

    logging.basicConfig(
        level=settings.logging.level_value,
        format=settings.logging.format,
        datefmt=settings.logging.date_format,
    )
    yield

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
app.include_router(api_router)


@app.get("/")
async def ping():
    return {"msg": "Hello, World!"}
