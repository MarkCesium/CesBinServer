from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime

from .base import Base


class Paste(Base):
    path: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(True), server_default="NOW()")
    expire_at: Mapped[datetime | None] = mapped_column(DateTime(True), nullable=True)
