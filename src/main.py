from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api import paste_router
from src.core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(paste_router)


@app.get("/")
async def ping():
    return {"msg": "Hello, World!"}
