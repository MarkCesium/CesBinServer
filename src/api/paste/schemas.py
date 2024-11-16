from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class PasteCreate(BaseModel):
    text: str
    period: str | None = Field(default=None, min_length=5, max_length=20)


class PasteRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    expire_at: datetime | None = None
    # model_config = ConfigDict(from_attributes=True)
