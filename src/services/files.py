from aiofile import async_open
from src.core.config import BASE_DIR


async def get_paste_from_file(paste_path: str) -> str:
    async with async_open(paste_path, "rb") as file:
        return await file.read()


async def create_paste_file(paste_path: str, text: str) -> None:
    async with async_open(paste_path, "wb") as file:
        await file.write(text.encode())
        file.seek(0)
