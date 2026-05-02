from __future__ import annotations

from app.core.database import engine, init_database
from app.models.base import Base
from app.models.character import Character  # noqa: F401
from app.models.chat_session import ChatSession  # noqa: F401
from app.models.message import Message  # noqa: F401


def main() -> None:
    init_database()
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    main()
