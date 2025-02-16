from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import format_router, paste_router
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


app = FastAPI(lifespan=lifespan)
app.include_router(paste_router)
app.include_router(format_router)


@app.get("/")
async def ping():
    return {"msg": "Hello, World!"}
