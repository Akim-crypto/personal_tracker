"""Pydantic-схемы для API тем ресурсов заметок и прогресса"""

from __future__ import annotations
from pydantic import BaseModel,Field,HttpUrl
from typing import Literal


class TopicCreate(BaseModel):
    """Схема для создания новой темы"""
    title:str = Field(min_length=1,max_length=200)
    description:str = ""

class TopicRead(BaseModel):
    """схема для чтения информации о теме"""
    title:str
    description:str


class ResourceCreate(BaseModel):
    """схема для добавления ресурса к теме"""
    res_type: Literal["link","text"]
    content: str

class LinkResourceCreate(BaseModel):
    """специализированная схема для ресурса ссылки"""
    url: HttpUrl

class NoteCreate(BaseModel):
    """схема для добавления заметки к теме"""
    text: str = Field(min_length=1)

class ProgressCreate(BaseModel):
    """схема для добавления записи о прогрессе по теме"""
    percent: int = Field(ge=0, le=100)


# Здесь gt (greater than), ge (greater than or equal), lt (less than),
# le (less than or equal) используются для числовых ограничений.