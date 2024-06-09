from pydantic import BaseModel, ConfigDict


class PasteBase(BaseModel):
    text: str
    created_at: int


class PasteCreate(BaseModel):
    text: str


class Paste(PasteBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
