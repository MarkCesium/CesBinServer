from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Interval


class Period(Base):
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    duration: Mapped[Interval] = mapped_column(Interval, nullable=False)
