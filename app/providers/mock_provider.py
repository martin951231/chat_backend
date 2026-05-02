from __future__ import annotations

from app.core.config import settings
from app.providers.base import BaseProvider, LLMRequest, LLMResponse


class MockProvider(BaseProvider):
    name = "mock"

    def generate(self, request: LLMRequest) -> LLMResponse:
        prompt_hint = request.system_prompt or f"你正在扮演 {request.character_name}"
        history_count = len(request.messages)
        content = (
            f"【Mock Reply】我是 {request.character_name}。\n"
            f"我收到了你的消息：{request.user_message}\n"
            f"当前上下文消息数：{history_count}。\n"
            f"角色设定参考：{prompt_hint[:120]}"
        )
        return LLMResponse(
            content=content,
            provider=self.name,
            model=settings.default_llm_model,
            finish_reason="stop",
            raw_response={
                "request_session_id": request.session_id,
                "message_count": history_count,
                "mocked": True,
            },
        )
