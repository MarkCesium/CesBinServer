from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime

from .base import Base


class Paste(Base):
    path: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(True), server_default="NOW()")
    expire_at: Mapped[datetime | None] = mapped_column(DateTime(True), nullable=True)
    format_id: Mapped[int] = mapped_column(ForeignKey("Format.id"), nullable=False)

    format = relationship("Format", back_populates="pastes")
