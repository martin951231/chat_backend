from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SessionCreate(BaseModel):
    character_code: str = Field(..., min_length=1, max_length=100, description="角色编码")
    title: str | None = Field(default=None, max_length=255)

class SessionUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="会话标题")

class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_code: str
    title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class SessionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_code: str
    title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
