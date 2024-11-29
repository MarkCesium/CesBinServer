from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    db_url: str | None = None
    db_sync_url: str | None = None
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    db_echo: bool = False

    rabbitmq_url: str | None = None
    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
settings.db_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
settings.db_sync_url = f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
settings.rabbitmq_url = f"pyamqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}"
