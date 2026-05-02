from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.character import Character


class CharacterRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Character]:
        statement = select(Character).order_by(Character.created_at.desc(), Character.id.desc())
        return list(self.db.scalars(statement).all())

    def get_by_id(self, character_id: int) -> Character | None:
        statement = select(Character).where(Character.id == character_id)
        return self.db.scalar(statement)

    def get_by_name(self, name: str) -> Character | None:
        statement = select(Character).where(Character.name == name)
        return self.db.scalar(statement)

    def create(self, payload: dict[str, object]) -> Character:
        character = Character(**payload)
        self.db.add(character)
        self.db.flush()
        return character
