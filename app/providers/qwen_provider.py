from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings
from app.core.logger import get_logger
from app.providers.base import BaseProvider, LLMRequest, LLMResponse

logger = get_logger(__name__)


class QwenProvider(BaseProvider):
    name = "qwen"

    @staticmethod
    def _normalize_message_content(value: Any) -> str:
        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if isinstance(value, list):
            parts: list[str] = []
            for item in value:
                if isinstance(item, str):
                    parts.append(item)
                    continue

                if isinstance(item, dict):
                    text = item.get("text") or item.get("content")
                    if isinstance(text, str):
                        parts.append(text)
            return "".join(parts)

        if isinstance(value, dict):
            text = value.get("text") or value.get("content")
            if isinstance(text, str):
                return text

        return str(value)

    def generate(self, request: LLMRequest) -> LLMResponse:
        url = settings.ai_base_url
        api_key = settings.ai_api_key
        configured_model = settings.ai_model
        temperature = request.temperature if request.temperature is not None else settings.ai_temperature
        request_timeout = settings.ai_timeout

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        messages: list[dict[str, str]] = []

        if request.system_prompt:
            messages.append({
                "role":'system',
                "content":request.system_prompt
            })

        for message in request.messages:
            messages.append({
                 "role":message.role,
                 "content":message.content,
            })

        messages.append(
            {
                "role": "user",
                "content": request.user_message,
            }
        )

        payload = {
            "model": configured_model,
            "messages": messages,
            "temperature": temperature,
            "enable_thinking": settings.ai_enable_thinking,
        }
        if request.top_p is not None:
            payload["top_p"] = request.top_p
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        if settings.ai_thinking_budget is not None:
            payload["thinking_budget"] = settings.ai_thinking_budget

        try:
            with httpx.Client(timeout=request_timeout) as client:
                response = client.post(
                    url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
                choice = result["choices"][0]
                message = choice["message"]

                reply = self._normalize_message_content(message.get("content"))
                reasoning_content = self._normalize_message_content(message.get("reasoning_content")) or None
                finish_reason = choice.get("finish_reason", "stop")
                actual_model = str(result.get("model") or configured_model)

                logger.info(
                    "Qwen response model=%s finish_reason=%s content_length=%s reasoning_length=%s",
                    actual_model,
                    finish_reason,
                    len(reply),
                    len(reasoning_content or ""),
                )

                if not reply:
                    raise Exception(
                        "Qwen response content is empty "
                        f"(model={actual_model}, finish_reason={finish_reason}, "
                        f"reasoning_length={len(reasoning_content or '')})"
                    )

                return LLMResponse(
                    content=reply,
                    provider=self.name,
                    model=actual_model,
                    finish_reason=finish_reason,
                    reasoning_content=reasoning_content,
                    raw_response=result,
                )

        except httpx.TimeoutException as e:
            raise Exception("请求超时") from e
        except httpx.HTTPStatusError as e:
            error_text = e.response.text
            raise Exception(f"Qwen HTTP 请求失败: {e.response.status_code} - {error_text}") from e
        except KeyError as e:
            raise Exception(f"Qwen 响应结构解析失败，缺少字段: {e}") from e
