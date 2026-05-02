from __future__ import annotations

from app.core.config import settings
from app.models.character import Character
from app.models.message import Message
from app.providers.base import LLMRequest, LLMResponse, ProviderMessage
from app.providers.provider_factory import ProviderFactory
from app.services.character_service import CharacterService


class LLMService:
    def __init__(self, provider_name: str | None = None) -> None:
        self.provider_name = provider_name or settings.default_llm_provider
        self.character_service = CharacterService()

    def generate_reply(
        self,
        *,
        character_code: str,
        session_id: int,
        messages: list[Message],
        user_message: str,
        provider_name: str | None = None,
    ) -> LLMResponse:
        character = self.character_service.get_character_by_code(character_code)

        final_provider_name = provider_name or self.provider_name
        provider = ProviderFactory.create(final_provider_name)

        final_system_prompt = (
            f"# 系统设定\n{character.prompt.system_prompt}\n\n"
            f"# 角色补充设定\n{character.prompt.role_prompt}"
        ).strip()

        request = LLMRequest(
            character_name=character.name,
            system_prompt=final_system_prompt,
            user_message=user_message,
            session_id=session_id,
            messages=[
                ProviderMessage(role=message.role, content=message.content)
                for message in messages
            ],
            temperature=character.llm.temperature,
            top_p=character.llm.top_p,
            max_tokens=character.llm.max_tokens,
            model=character.llm.model,
            metadata={"character_code": character.code},
        )
        return provider.generate(request)
