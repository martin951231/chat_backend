from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProviderMessage:
    role: str
    content: str


@dataclass(slots=True)
class LLMRequest:
    character_name: str
    system_prompt: str | None
    user_message: str
    session_id: int
    messages: list[ProviderMessage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    model: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LLMResponse:
    content: str
    provider: str
    model: str
    finish_reason: str = "stop"
    reasoning_content: str | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    name: str = "base"

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError
