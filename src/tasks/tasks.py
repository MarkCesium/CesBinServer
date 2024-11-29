import os

from .celery import celery_app
from src.core.db_helper import db_helper
from src.core.models import Paste
from src.core.repositories import PasteSyncRepository
from src.core.config import BASE_DIR


@celery_app.task
def delete_paste(id: int) -> None:
    with db_helper.sync_session_factory() as session:
        paste: Paste = PasteSyncRepository.get_by_id(session, id)
        os.remove(str(BASE_DIR / paste.path))
        session.delete(paste)
        session.commit()
