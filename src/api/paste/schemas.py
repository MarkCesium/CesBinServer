from pydantic import BaseModel, ConfigDict


class PasteCreate(BaseModel):
    text: str


class PasteRead(BaseModel):
    id: str
    text: str
    created_at: int
    model_config = ConfigDict(from_attributes=True)
