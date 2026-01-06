"""Скрипт иницилизации базы данных

Создает все таблицы описанные в ORM моделях
"""

from __future__ import annotations

from app.db.database import Base , engine
from app.db import models

def init_db() -> None:
    """Создает таблицы в базе данных если они еще не существуют"""
    Base.metadata.create_all(bind=engine)
    