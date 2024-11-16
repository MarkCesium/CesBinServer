from pydantic import BaseModel, Field
from datetime import datetime


class PasteCreate(BaseModel):
    text: str
    period: str | None = Field(default=None, min_length=5, max_length=20)
    format: str | None = Field(default="plain", min_length=2, max_length=20)


class PasteRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    expire_at: datetime | None = None
    format: str
