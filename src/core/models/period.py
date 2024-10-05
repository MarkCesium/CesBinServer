from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Interval


class Period(Base):
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    duration: Mapped[Interval] = mapped_column(Interval, nullable=False)
    paste = relationship("Paste", back_populates="Period")
