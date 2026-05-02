from __future__ import annotations

from app.core.config_loader import load_character_config
from app.schemas.character import CharacterCard, CharacterConfig, CharacterConfigFile

class CharacterService:
    def __init__(self) -> None:
        raw_config = load_character_config()
        self.config = CharacterConfigFile.model_validate(raw_config)
    def list_characters(self) -> list[CharacterCard]:
        return [
            CharacterCard(
                code=character.code,
                name=character.name,
                avatar=character.avatar,
                description=character.description,
                background=character.personality.background,
                speaking_style=character.personality.speaking_style,
                traits=character.personality.traits,
            )
            for character in self.config.characters
        ]
    def get_character_by_code(self, code: str) -> CharacterConfig:
        for character in self.config.characters:
            if character.code == code:
                return character
        raise ValueError(f"未找到角色配置: {code}")