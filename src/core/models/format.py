from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Format(Base):
    __tablename__ = "formats"
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    pastes = relationship("Paste", back_populates="format")
