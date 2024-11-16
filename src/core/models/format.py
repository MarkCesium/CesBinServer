from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String

from .base import Base


class Format(Base):
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    pastes = relationship("Paste", back_populates="format")
