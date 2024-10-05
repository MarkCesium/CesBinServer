from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey


class Paste(Base):
    paste_path: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    expire_at: Mapped[int | None] = mapped_column(Integer, nullable=True)
    period_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("Period.id"), nullable=True
    )
    expiration_period = relationship("Period", back_populates="Paste")
