from __future__ import annotations

from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None


def success_response(data: Any = None, message: str = "success", code: int = 200) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "data": jsonable_encoder(data),
    }


def error_response(message: str, code: int, data: Any = None) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "data": jsonable_encoder(data),
    }
