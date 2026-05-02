from __future__ import annotations

from app.core.exceptions import BadRequestException
from app.providers.base import BaseProvider
from app.providers.mock_provider import MockProvider
from app.providers.qwen_provider import QwenProvider


class ProviderFactory:
    _providers: dict[str, type[BaseProvider]] = {
        "mock": MockProvider,
        "qwen": QwenProvider,
        # Future extension:
        # "openai": OpenAIProvider,
        # "deepseek": DeepSeekProvider,
        # "qwen": QwenProvider,
    }

    @classmethod
    def create(cls, provider_name: str) -> BaseProvider:
        provider_class = cls._providers.get(provider_name)
        if provider_class is None:
            raise BadRequestException(message=f"不支持的 provider: {provider_name}")
        return provider_class()
