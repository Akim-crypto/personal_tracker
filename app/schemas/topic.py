"""Pydantic-схемы для API тем ресурсов заметок и прогресса"""

from __future__ import annotations
from pydantic import BaseModel,Field,HttpUrl
from typing import Literal


class TopicCreate(BaseModel):
    title:str = Field(min_length=1,max_length=200)
    description:str = ""

class TopicRead(BaseModel):
    title:str
    description:str


class ResourceCreate(BaseModel):
    res_type: Literal["link","text"]
    content: str

class LinkResourceCreate(BaseModel):
    url: HttpUrl

class NoteCreate(BaseModel):
    text: str = Field(min_length=1)

class ProgressCreate(BaseModel):
    percent: int = Field(ge=0, le=100)


# Здесь gt (greater than), ge (greater than or equal), lt (less than),
# le (less than or equal) используются для числовых ограничений.