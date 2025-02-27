import logging
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, status

from src.providers import get_paste_service

from . import schemas

if TYPE_CHECKING:
    from src.services import PasteService

router = APIRouter(prefix="/paste", tags=["Paste"])
logger = logging.getLogger(__name__)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_paste(
    id: int,
    paste_service: Annotated["PasteService", Depends(get_paste_service)],
) -> schemas.PasteRead:
    return await paste_service.get(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_paste(
    paste: schemas.PasteCreate,
    paste_service: Annotated["PasteService", Depends(get_paste_service)],
) -> schemas.PasteRead:
    paste = await paste_service.create(paste.text, paste.format, paste.period)

    return await paste_service.get(paste.id)