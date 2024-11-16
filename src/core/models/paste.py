from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Paste(Base):
    paste_path: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    expire_at: Mapped[int | None] = mapped_column(Integer, nullable=True)
