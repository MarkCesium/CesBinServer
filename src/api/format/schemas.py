from pydantic import BaseModel


class FormatRead(BaseModel):
    id: int
    name: str
