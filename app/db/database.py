"""Модуль для настройки подключения к базе данных SQLITE и создания сесси

Используется FAST-API приложением для работы с SQLAlchemy
"""


from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Session


DATABASE_URL = "sqlite:///./data/tracker.db"

class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей
    
    Используется как родитель для декларативных моделей SQLCHEMY
    """

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False},
)

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Generator[Session,None,None]:
    """
    Зависимость FASTAPI для получения сессии БД на запрос
    
    Создает новую сессию перед обработкой запроса и закрывает ее после завершения
    
    Yields
        Экземпляр Session для работы с БД
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()