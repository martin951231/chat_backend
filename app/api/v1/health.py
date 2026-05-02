from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.core.database import check_database_connection
from app.core.response import ApiResponse, success_response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=ApiResponse[dict[str, str]])
def health_check() -> dict[str, object]:
    database_status = "up"
    try:
        check_database_connection()
    except Exception:
        database_status = "down"

    return success_response(
        data={
            "status": "ok",
            "database": database_status,
            "provider": settings.default_llm_provider,
        }
    )
