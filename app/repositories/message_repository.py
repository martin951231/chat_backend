from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_session_id(self, session_id: int) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.asc(), Message.id.asc())
        )
        return list(self.db.scalars(statement).all())

    def create(self, payload: dict[str, object]) -> Message:
        message = Message(**payload)
        self.db.add(message)
        self.db.flush()
        return message
