from pydantic import BaseModel, ConfigDict


class PasteCreate(BaseModel):
    title: str
    text: str
    expire_at: int | None = None


class PasteRead(BaseModel):
    id: str
    title: str
    text: str
    created_at: int
    expire_at: int | None = None
    model_config = ConfigDict(from_attributes=True)
