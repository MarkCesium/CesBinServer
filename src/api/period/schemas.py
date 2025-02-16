
from pydantic import BaseModel


class PeriodRead(BaseModel):
    id: int
    name: str
