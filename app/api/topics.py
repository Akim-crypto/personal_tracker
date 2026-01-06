"""
API-роуты для работы с темами, ресурсами, заметками и прогрессом.

На этом этапе темы хранятся в базе данных SQLite через SQLAlchemy.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.topic import TopicCreate, TopicRead
from app.services import topic_service

router = APIRouter(
    prefix="/topics",
    tags=["topics"],
)


@router.get("", response_model=list[TopicRead])
def list_topics(db: Session = Depends(get_db)) -> list[TopicRead]:
    """
    Возвращает список всех тем.

    Args:
        db: Сессия базы данных, предоставленная через Depends.

    Returns:
        Список тем в виде схем TopicRead.
    """
    topics = topic_service.get_topics(db)
    return [
        TopicRead(title=t.title, description=t.description)
        for t in topics
    ]


@router.post("", response_model=TopicRead, status_code=201)
def create_topic(
    payload: TopicCreate,
    db: Session = Depends(get_db),
) -> TopicRead:
    """
    Создаёт новую тему.

    Args:
        payload: Данные для создания темы.
        db: Сессия базы данных.

    Returns:
        Созданная тема в виде схемы TopicRead.

    Raises:
        HTTPException: Если тема с таким названием уже существует.
    """
    existing = topic_service.get_topic_by_title(db, payload.title)
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Тема уже существует",
        )

    topic = topic_service.create_topic(db, payload)
    return TopicRead(title=topic.title, description=topic.description)


@router.get("/{title}", response_model=TopicRead)
def get_topic(
    title: str,
    db: Session = Depends(get_db),
) -> TopicRead:
    """
    Возвращает тему по названию.

    Args:
        title: Название темы.
        db: Сессия базы данных.

    Returns:
        Найденная тема в виде схемы TopicRead.

    Raises:
        HTTPException: Если тема не найдена (404).
    """
    topic = topic_service.get_topic_by_title(db, title)
    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Тема не найдена",
        )
    return TopicRead(title=topic.title, description=topic.description)
