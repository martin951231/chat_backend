from __future__ import annotations

from os import path
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CHARACTER_CONFIG_FILE = DATA_DIR / "characters.yaml"

def load_yaml_config(file_path: Path | str) -> dict[str,any]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError("YAML 配置格式错误，根节点必须是对象")

    return data

def load_character_config() -> dict[str, Any]:
    return load_yaml_config(CHARACTER_CONFIG_FILE)


character_config = load_character_config()