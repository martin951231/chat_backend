from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import NotFoundException
from app.models.chat_session import ChatSession
from app.repositories.message_repository import MessageRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.chat import ChatHistoryMessage, ChatRequest, ChatResponse, MessageRead
from app.schemas.session import SessionCreate, SessionListItem, SessionRead, SessionUpdate
from app.services.character_service import CharacterService
from app.services.llm_service import LLMService


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.session_repository = SessionRepository(db)
        self.message_repository = MessageRepository(db)
        self.llm_service = LLMService()
        self.character_service = CharacterService()

    def list_sessions(self) -> list[SessionListItem]:
        sessions = self.session_repository.list_active()
        return [SessionListItem.model_validate(session) for session in sessions]

    def create_session(self, payload: SessionCreate) -> SessionRead:
        try:
            character = self.character_service.get_character_by_code(payload.character_code)
            if character is None:
                raise NotFoundException(message=f"角色不存在: {payload.character_code}")

            title = payload.title or f"{payload.character_code} - 新的会话"

            session = self.session_repository.create(
                {
                    "character_code": payload.character_code,
                    "title": title,
                    "is_active": True,
                }
            )

            self.db.commit()
            self.db.refresh(session)

            return SessionRead.model_validate(session)
        except Exception:
            self.db.rollback()
            raise

    def rename_session(self, session_id: int, payload: SessionUpdate) -> SessionRead:
        try:
            session = self.session_repository.get_by_id(session_id)
            if session is None:
                raise NotFoundException(message=f"会话不存在: {session_id}")

            updated_session = self.session_repository.update_title(session, payload.title)

            self.db.commit()
            self.db.refresh(updated_session)

            return SessionRead.model_validate(updated_session)
        except Exception:
            self.db.rollback()
            raise

    def delete_session(self, session_id: int) -> SessionRead:
        try:
            session = self.session_repository.get_by_id(session_id)
            if session is None:
                raise NotFoundException(message=f"会话不存在: {session_id}")

            deleted_session = self.session_repository.soft_delete(session)

            self.db.commit()
            self.db.refresh(deleted_session)

            return SessionRead.model_validate(deleted_session)
        except Exception:
            self.db.rollback()
            raise

    def get_session_messages(self, session_id: int) -> list[MessageRead]:
        session = self.session_repository.get_by_id(session_id)
        if session is None:
            raise NotFoundException(message=f"会话不存在: {session_id}")

        messages = self.message_repository.list_by_session_id(session_id)
        return [MessageRead.model_validate(message) for message in messages]

    def send_message(self, payload: ChatRequest) -> ChatResponse:
        try:
            # 1. 查 YAML 角色配置
            character = self.character_service.get_character_by_code(payload.character_code)
            if character is None:
                raise NotFoundException(message=f"角色不存在: {payload.character_code}")

            # 2. 查/建会话
            session = self._resolve_session(character_code=character.code, payload=payload)

            # 3. 保存用户消息
            user_message = self.message_repository.create(
                {
                    "session_id": session.id,
                    "role": "user",
                    "content": payload.message,
                }
            )

            # 4. 组装历史消息
            history_messages = self.message_repository.list_by_session_id(session.id)

            max_context_message = settings.ai_max_context_message or 10

            valid_history_messages = [
                message
                for message in history_messages
                if message.role in {"user", "assistant"}
            ]

            recent_history_messages = valid_history_messages[-max_context_message:]

            history = [
                ChatHistoryMessage(role=message.role, content=message.content)
                for message in recent_history_messages
            ]

            # 5. 调用 LLM
            llm_response = self.llm_service.generate_reply(
                character_code=character.code,
                session_id=session.id,
                messages=history,
                user_message=payload.message,
                provider_name="qwen",
            )

            # 6. 保存 assistant 消息
            assistant_message = self.message_repository.create(
                {
                    "session_id": session.id,
                    "role": "assistant",
                    "content": llm_response.content,
                    "provider_name": llm_response.provider,
                    "model_name": llm_response.model,
                }
            )

            # 7. 提交事务
            session.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(session)
            self.db.refresh(user_message)
            self.db.refresh(assistant_message)

            return ChatResponse(
                reply=llm_response.content,
                provider=llm_response.provider,
                model=llm_response.model,
                finish_reason=llm_response.finish_reason,
                reasoning_content=llm_response.reasoning_content,
                raw_response=llm_response.raw_response,
                session=SessionRead.model_validate(session),
                user_message=MessageRead.model_validate(user_message),
                assistant_message=MessageRead.model_validate(assistant_message),
                character_code=character.code,
            )
        except Exception:
            self.db.rollback()
            raise

    def _resolve_session(self, *, character_code: str, payload: ChatRequest) -> ChatSession:
        if payload.session_id is not None:
            session = self.session_repository.get_by_id(payload.session_id)
            if session is None:
                raise NotFoundException(message=f"会话不存在: {payload.session_id}")

            if session.character_code != character_code:
                raise NotFoundException(message=f"会话不属于当前角色: {payload.session_id}")

            return session

        title = payload.session_title or self._build_session_title(character_code, payload.message)
        return self.session_repository.create(
            {
                "character_code": character_code,
                "title": title,
                "is_active": True,
            }
        )

    @staticmethod
    def _build_session_title(character_code: str, user_message: str) -> str:
        clean_title = user_message.strip().replace("\n", " ")
        short_title = clean_title[:30] if clean_title else f"与 {character_code} 的对话"
        return f"{character_code} - {short_title}"