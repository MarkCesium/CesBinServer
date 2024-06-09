from fastapi import FastAPI
from src.api import paste_router

app = FastAPI()
app.include_router(paste_router)


@app.get("/")
async def ping():
    return {"msg": "Hello, World!"}
