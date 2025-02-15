import os

from aiofile import async_open


class FileService:
    @classmethod
    async def get(cls, path: str) -> str:
        async with async_open(path, "rb") as file:
            return await file.read()

    @classmethod
    async def create(cls, path: str, text: str) -> None:
        async with async_open(path, "wb") as file:
            await file.write(text.encode())
            file.seek(0)

    @classmethod
    def delete(cls, path: str) -> None:
        os.remove(path)
