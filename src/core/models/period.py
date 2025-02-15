from sqlalchemy import Interval, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Period(Base):
    __tablename__ = "periods"
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    duration: Mapped[Interval] = mapped_column(Interval, nullable=False)
