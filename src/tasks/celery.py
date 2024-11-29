from celery import Celery

from src.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.rabbitmq_url,
    include=["src.tasks.tasks"],
)
