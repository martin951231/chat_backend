from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def _is_sqlite(database_url: str) -> bool:
    return database_url.startswith("sqlite")


def _build_engine() -> Engine:
    connect_args: dict[str, object] = {}
    if _is_sqlite(settings.database_url):
        connect_args["check_same_thread"] = False

    return create_engine(
        settings.database_url,
        echo=settings.database_echo,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


engine = _build_engine()
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def init_database() -> None:
    if _is_sqlite(settings.database_url) and ":memory:" not in settings.database_url:
        sqlite_path = settings.database_url.replace("sqlite:///", "", 1)
        target_path = Path(sqlite_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Database initialized with url: %s", settings.database_url)


def check_database_connection() -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
