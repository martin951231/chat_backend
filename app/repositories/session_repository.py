from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


class SessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[ChatSession]:
        statement = (
            select(ChatSession)
            .where(ChatSession.is_active.is_(True))
            .order_by(ChatSession.updated_at.desc(), ChatSession.id.desc())
        )
        return list(self.db.scalars(statement).all())

    def list_by_character_id(self, character_code: str) -> list[ChatSession]:
        statement = (
            select(ChatSession)
            .where(
                ChatSession.character_code == character_code,
                ChatSession.is_active.is_(True),
            )
            .order_by(ChatSession.updated_at.desc(), ChatSession.id.desc())
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, session_id: int) -> ChatSession | None:
        statement = (
            select(ChatSession)
            .where(
                ChatSession.id == session_id,
                ChatSession.is_active.is_(True),
            )
        )
        return self.db.scalar(statement)

    def create(self, payload: dict[str, object]) -> ChatSession:
        session = ChatSession(**payload)
        self.db.add(session)
        self.db.flush()
        return session

    def update_title(self, session: ChatSession, title: str) -> ChatSession:
        session.title = title
        self.db.flush()
        return session

    def soft_delete(self, session: ChatSession) -> ChatSession:
        session.is_active = False
        self.db.flush()
        return session