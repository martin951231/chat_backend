from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.character import router as character_router
from app.api.v1.chat import router as chat_router
from app.api.v1.health import router as health_router
from app.api.v1.session import router as session_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(health_router)
api_router.include_router(character_router)
api_router.include_router(session_router)
api_router.include_router(chat_router)
