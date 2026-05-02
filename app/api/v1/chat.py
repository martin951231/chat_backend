from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response
from app.schemas.chat import ChatRequest
from app.schemas.session import SessionCreate, SessionUpdate
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(db)


@router.get("/sessions")
def list_sessions(
    service: ChatService = Depends(get_chat_service),
):
    data = service.list_sessions()
    return success_response(data=data)


@router.post("/sessions")
def create_session(
    payload: SessionCreate,
    service: ChatService = Depends(get_chat_service),
):
    data = service.create_session(payload)
    return success_response(data=data)


@router.patch("/sessions/{session_id}")
def rename_session(
    session_id: int,
    payload: SessionUpdate,
    service: ChatService = Depends(get_chat_service),
):
    data = service.rename_session(session_id, payload)
    return success_response(data=data)


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    service: ChatService = Depends(get_chat_service),
):
    data = service.delete_session(session_id)
    return success_response(data=data)


@router.get("/sessions/{session_id}/messages")
def get_session_messages(
    session_id: int,
    service: ChatService = Depends(get_chat_service),
):
    data = service.get_session_messages(session_id)
    return success_response(data=data)


@router.post("/messages")
def send_message(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    data = service.send_message(payload)
    return success_response(data=data)