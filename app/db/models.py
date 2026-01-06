"""
ORM-модели SQLAlchemy для хранения данных трекера в БД.

Пока реализована только модель Topic.
"""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TopicModel(Base):
    """
    ORM-модель темы для изучения.

    Хранится в таблице topics.
    """

    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        doc="Уникальный идентификатор темы.",
    )
    title: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
        doc="Название темы.",
    )
    description: Mapped[str] = mapped_column(
        String(500),
        default="",
        doc="Краткое описание темы.",
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление модели.

        Returns:
            Строка с основными полями темы.
        """
        return f"TopicModel(id={self.id!r}, title={self.title!r})"
