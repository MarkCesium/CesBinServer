from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Paste(Base):
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    expire_at: Mapped[int | None] = mapped_column(Integer, nullable=True)
