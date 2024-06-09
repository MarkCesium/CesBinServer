from .base import Base
from sqlalchemy.orm import Mapped


class Paste(Base):
    text: Mapped[str]
    created_at: Mapped[int]
