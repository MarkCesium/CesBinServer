from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    db_url: str | None = None
    db_user: str
    db_pass: str
    db_name: str
    db_echo: bool = False


settings = Settings()
settings.db_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@cesbin-database/{settings.db_name}"
