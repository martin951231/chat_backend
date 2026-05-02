from __future__ import annotations

from fastapi import APIRouter

from app.core.response import ApiResponse, success_response
from app.schemas.character import CharacterCard
from app.services.character_service import CharacterService

router = APIRouter(prefix="/characters", tags=["characters"])


def get_character_service() -> CharacterService:
    return CharacterService()


@router.get("", response_model=ApiResponse[list[CharacterCard]])
def list_characters() -> dict[str, object]:
    service = get_character_service()
    characters = service.list_characters()
    data = [item.model_dump() for item in characters]
    return success_response(data=data)
