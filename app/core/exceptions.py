from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.core.response import error_response

logger = get_logger(__name__)


class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: int = 40000,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message: str = "请求参数错误", detail: Any = None) -> None:
        super().__init__(
            message=message,
            code=40000,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class NotFoundException(AppException):
    def __init__(self, message: str = "资源不存在", detail: Any = None) -> None:
        super().__init__(
            message=message,
            code=40400,
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ConflictException(AppException):
    def __init__(self, message: str = "资源冲突", detail: Any = None) -> None:
        super().__init__(
            message=message,
            code=40900,
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(message=exc.message, code=exc.code, data=exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response(
                message="请求参数校验失败",
                code=42200,
                data=exc.errors(),
            ),
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                message=str(exc.detail),
                code=exc.status_code,
                data=None,
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception occurred: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response(
                message="服务器内部错误",
                code=50000,
                data=None,
            ),
        )
