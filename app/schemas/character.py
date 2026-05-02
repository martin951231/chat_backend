from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class PersonalityConfig(BaseModel):
    traits: List[str] = Field(default_factory=list)
    background: str = ""
    speaking_style: str = ""


class LLMConfig(BaseModel):
    model: str = "qwen3-max-2026-01-23"
    temperature: float = 0.8
    top_p: float = 0.9
    max_tokens: int = 1000


class PromptConfig(BaseModel):
    system_prompt: str = ""
    role_prompt: str = ""


class CharacterConfig(BaseModel):
    code: str
    name: str
    avatar: str = ""
    description: str = ""
    personality: PersonalityConfig
    llm: LLMConfig
    prompt: PromptConfig


class DefaultLLMConfig(BaseModel):
    temperature: float = 0.8
    top_p: float = 0.9
    max_tokens: int = 1000


class DefaultsConfig(BaseModel):
    llm: DefaultLLMConfig


class CharacterConfigFile(BaseModel):
    version: str = "1.0"
    default_model: str = "qwen3-max-2026-01-23"
    defaults: DefaultsConfig
    characters: List[CharacterConfig] = Field(default_factory=list)


class CharacterCard(BaseModel):
    code: str
    name: str
    avatar: str = ""
    description: str = ""
    background: str = ""
    speaking_style: str = ""
    traits: List[str] = Field(default_factory=list)