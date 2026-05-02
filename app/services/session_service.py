from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.chat_session import ChatSession
from app.repositories.character_repository import CharacterRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.session import SessionCreate


class SessionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.character_repository = CharacterRepository(db)
        self.session_repository = SessionRepository(db)

    def list_sessions_by_character(self, character_id: int) -> list[ChatSession]:
        character = self.character_repository.get_by_id(character_id)
        if character is None:
            raise NotFoundException(message=f"角色不存在: {character_id}")

        return self.session_repository.list_by_character_id(character_id)

    def create_session(self, payload: SessionCreate) -> ChatSession:
        character = self.character_repository.get_by_id(payload.character_id)
        if character is None:
            raise NotFoundException(message=f"角色不存在: {payload.character_id}")

        title = payload.title or f"与 {character.name} 的新会话"
        session = self.session_repository.create(
            {
                "character_id": payload.character_id,
                "title": title,
                "is_active": True,
            }
        )
        self.db.commit()
        self.db.refresh(session)
        return session
