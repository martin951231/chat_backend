from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="AI Character Platform Backend", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    ai_base_url: str
    ai_api_key: str
    ai_model: str
    ai_timeout: float = 600.0
    ai_temperature: float = 0.7
    ai_max_context_message: int = 10

    ai_enable_thinking: bool = Field(default=False, alias="AI_ENABLE_THINKING")
    ai_thinking_budget: int | None = Field(default=None, alias="AI_THINKING_BUDGET")

    database_url: str = Field(default="sqlite:///./data/ai_character.db", alias="DATABASE_URL")
    database_echo: bool = Field(default=False, alias="DATABASE_ECHO")

    default_llm_provider: str
    default_llm_model: str

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    cors_allow_origins: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins(self) -> list[str]:
        raw_value = self.cors_allow_origins.strip()
        if raw_value == "*":
            return ["*"]
        return [item.strip() for item in raw_value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
