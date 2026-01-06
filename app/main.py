"""
Точка входа FastAPI-приложения для персонального трекера прогресса.

Приложение предоставляет REST API для работы с темами, ресурсами,
заметками и прогрессом.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.topics import router as topics_router


def create_app() -> FastAPI:
    """
    Создаёт и настраивает экземпляр FastAPI-приложения.

    Returns:
        Инициализированный объект FastAPI.
    """
    app = FastAPI(
        title="Personal Tracker API",
        version="0.1.0",
        description="API для управления темами, ресурсами и прогрессом обучения.",
    )

    app.include_router(topics_router)

    @app.get("/health")
    def health() -> dict:
        """
        Простой health-check эндпоинт.

        Returns:
            Словарь со статусом сервиса.
        """
        return {"status": "ok"}

    return app


app = create_app()
