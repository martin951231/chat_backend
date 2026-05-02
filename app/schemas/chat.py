from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.session import SessionRead


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="历史消息角色")
    content: str = Field(..., min_length=1, description="历史消息内容")


class ChatRequest(BaseModel):
    character_code: str = Field(..., min_length=1, description="角色编码")
    session_id: int | None = Field(default=None, gt=0, description="会话ID")
    message: str = Field(..., min_length=1, description="用户消息")
    session_title: str | None = Field(default=None, max_length=255, description="会话标题")
    history: list[ChatHistoryMessage] = Field(default_factory=list, description="历史消息")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="模型回复")
    provider: str = Field(..., description="提供商")
    model: str = Field(..., description="模型名")
    finish_reason: str | None = Field(default=None, description="结束原因")
    reasoning_content: str | None = Field(default=None, description="模型思考内容")
    raw_response: dict[str, Any] | None = Field(default=None, description="原始响应")
    session: SessionRead = Field(..., description="当前会话")
    user_message: MessageRead = Field(..., description="本次用户消息")
    assistant_message: MessageRead = Field(..., description="本次助手消息")
    character_code: str = Field(..., description="角色编码")

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    role: str
    content: str
    provider_name: str | None = None
    model_name: str | None = None
    created_at: datetime
    updated_at: datetime

