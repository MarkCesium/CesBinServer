from pydantic import BaseModel, ConfigDict
from enum import Enum


class Period(str, Enum):
    # TODO: Rewrite! Get Periods from DataBase
    one_hour = "1 hour"
    three_hours = "3 hours"
    one_day = "1 day"
    one_week = "1 week"
    one_month = "1 month"
    three_months = "3 months"
    six_months = "6 months"
    one_year = "1 year"


class PasteCreate(BaseModel):
    text: str
    period: Period | None = None


class PasteRead(BaseModel):
    id: int
    text: str
    created_at: int
    expire_at: int | None = None
    model_config = ConfigDict(from_attributes=True)
