from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, status

from src.providers import get_format_repository

from . import schemas

if TYPE_CHECKING:
    from src.core.repositories import FormatRepository

router = APIRouter(prefix="/format", tags=["Format"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_formats(
    format_repository: Annotated["FormatRepository", Depends(get_format_repository)],
) -> list[schemas.FormatRead]:
    return await format_repository.get_all()
