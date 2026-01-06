"""
Точка входа FastAPI-приложения для персонального трекера.

Создаёт приложение, подключает роутеры и инициализирует базу данных.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.topics import router as topics_router
from app.db.init_db import init_db


def create_app() -> FastAPI:
    """
    Создаёт и настраивает экземпляр FastAPI-приложения.

    Returns:
        Инициализированный объект FastAPI.
    """
    init_db()

    app = FastAPI(
        title="Personal Tracker API",
        version="0.2.0",
        description=(
            "API для управления темами, ресурсами и прогрессом обучения. "
            "На этом этапе темы хранятся в SQLite через SQLAlchemy."
        ),
    )

    app.include_router(topics_router)

    @app.get("/health")
    def health() -> dict:
        """
        Эндпоинт проверки состояния сервиса.

        Returns:
            Словарь со статусом приложения.
        """
        return {"status": "ok"}

    return app


app = create_app()
