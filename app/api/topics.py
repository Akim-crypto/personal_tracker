"""
API-роуты для работы с темами, ресурсами, заметками и прогрессом.
Пока используем существующий FileStorage (JSON), чтобы быстро поднять API.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from storage.file_storage import FileStorage
from models.topic import Topic
from models.resource import Resource
from models.note import Note
from models.progress import ProgressEntry
from core.utils import find_topic_by_title, validate_url

from app.schemas.topic import (
    TopicCreate, TopicRead,
    ResourceCreate, NoteCreate, ProgressCreate
)

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicRead])
def list_topics():
    """Возвращает список всех тем пользователя
    
    Returns
        список тем в виде схем TopicRead
    """
    storage = FileStorage("data/data.json")
    with storage.session() as user:
        return [TopicRead(title=t.title, description=t.description) for t in user.topics]


@router.post("", response_model=TopicRead, status_code=201)
def create_topic(payload: TopicCreate):
    """
    Создаёт новую тему.

    Если тема с таким названием уже существует, возвращает ошибку 409.

    Args:
        payload: Данные для создания темы.

    Returns:
        Созданная тема в виде схемы TopicRead.

    Raises:
        HTTPException: Если тема уже существует.
    """
    storage = FileStorage("data/data.json")
    with storage.session() as user:
        if find_topic_by_title(user, payload.title) is not None:
            raise HTTPException(status_code=409, detail="Тема уже существует")

        topic = Topic(title=payload.title, description=payload.description)
        user.add_topic(topic)
        return TopicRead(title=topic.title, description=topic.description)


@router.get("/{title}", response_model=TopicRead)
def get_topic(title: str):
    """
    Возвращает информацию о конкретной теме по названию.

    Args:
        title: Название темы.

    Returns:
        Схема TopicRead для найденной темы.

    Raises:
        HTTPException: Если тема не найдена (404).
    """
    storage = FileStorage("data/data.json")
    with storage.session() as user:
        topic = find_topic_by_title(user, title)
        if topic is None:
            raise HTTPException(status_code=404, detail="Тема не найдена")
        return TopicRead(title=topic.title, description=topic.description)


@router.post("/{title}/resources", status_code=201)
def add_resource(title: str, payload: ResourceCreate):
    """
    Добавляет ресурс к выбранной теме.

    Для ресурсов типа 'link' дополнительно проверяется валидность URL.

    Args:
        title: Название темы.
        payload: Данные ресурса (тип и содержимое).

    Returns:
        Словарь с полем ok=True при успешном добавлении.

    Raises:
        HTTPException:
            404 — если тема не найдена.
            422 — если URL не прошёл валидацию.
    """
    storage = FileStorage("data/data.json")
    with storage.session() as user:
        topic = find_topic_by_title(user, title)
        if topic is None:
            raise HTTPException(status_code=404, detail="Тема не найдена")

        if payload.res_type == "link" and not validate_url(payload.content):
            raise HTTPException(status_code=422, detail="Невалидный URL")

        topic.add_resource(Resource(res_type=payload.res_type, content=payload.content))
        return {"ok": True}


@router.post("/{title}/notes", status_code=201)
def add_note(title: str, payload: NoteCreate):
    """
    Добавляет заметку к выбранной теме.

    Args:
        title: Название темы.
        payload: Данные заметки.

    Returns:
        Словарь с полем ok=True при успешном добавлении.

    Raises:
        HTTPException:
            404 — если тема не найдена.
    """
    storage = FileStorage("data/data.json")
    with storage.session() as user:
        topic = find_topic_by_title(user, title)
        if topic is None:
            raise HTTPException(status_code=404, detail="Тема не найдена")

        topic.add_note(Note(text=payload.text))
        return {"ok": True}


@router.post("/{title}/progress", status_code=201)
def add_progress(title: str, payload: ProgressCreate):
    """
    Добавляет запись о прогрессе по выбранной теме.

    Args:
        title: Название темы.
        payload: Данные о прогрессе (процент).

    Returns:
        Словарь с полем ok=True при успешном добавлении.

    Raises:
        HTTPException:
            404 — если тема не найдена.
    """
    storage = FileStorage("data/data.json")
    with storage.session() as user:
        topic = find_topic_by_title(user, title)
        if topic is None:
            raise HTTPException(status_code=404, detail="Тема не найдена")

        topic.add_progress(ProgressEntry(percent=payload.percent))
        return {"ok": True}
