from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import init_database
from app.core.exceptions import register_exception_handlers
from app.core.logger import get_logger
from app.core.response import ApiResponse, success_response

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    logger.info("Application startup completed.")
    yield
    logger.info("Application shutdown completed.")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        started_at = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.info("%s %s -> %s (%sms)", request.method, request.url.path, response.status_code, duration_ms)
        return response

    @app.get("/", response_model=ApiResponse[dict[str, str]])
    def root() -> dict[str, object]:
        return success_response(
            data={
                "app": settings.app_name,
                "docs": "/docs",
                "openapi": "/openapi.json",
            }
        )

    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
