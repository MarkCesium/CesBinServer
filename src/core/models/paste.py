from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Paste(Base):
    __tablename__ = "pastes"
    path: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(True), server_default="NOW()")
    expire_at: Mapped[datetime | None] = mapped_column(DateTime(True), nullable=True)
    format_id: Mapped[int] = mapped_column(ForeignKey("formats.id"), nullable=False)

    format = relationship("formats", back_populates="pastes")
