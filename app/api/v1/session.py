from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.schemas.session import SessionCreate, SessionRead
from app.services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])


def get_session_service(db: Session = Depends(get_db)) -> SessionService:
    return SessionService(db)


@router.get("/{character_id}", response_model=ApiResponse[list[SessionRead]])
def list_sessions(
    character_id: int,
    service: SessionService = Depends(get_session_service),
) -> dict[str, object]:
    sessions = service.list_sessions_by_character(character_id)
    data = [SessionRead.model_validate(item) for item in sessions]
    return success_response(data=data)


@router.post("", response_model=ApiResponse[SessionRead], status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    service: SessionService = Depends(get_session_service),
) -> dict[str, object]:
    session = service.create_session(payload)
    return success_response(
        data=SessionRead.model_validate(session),
        message="会话创建成功",
    )
