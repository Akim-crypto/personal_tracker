"""
Модуль для работы с темами изучения
"""

from __future__ import annotations
from typing import List, Dict
from models.resource import Resource
from models.note import Note
from models.progress import ProgressEntry


class Topic:
    """
    класс темы для изучения

    содержит ресурсы , заметки и записи о прогрессе
    """

    def __init__(self,title:str,description:str =""):
        """
        Инициализация темы

        Args:
            title: Название темы
            description: Описание темы (опционально)
        """
        self.title = title
        self.description = description
        self.resources: List[Resource] = []
        self.notes: List[Note] =[]
        self.progress: List[ProgressEntry] = []

    def add_resource(self,res: Resource) -> None:
        """
        Добавляет ресурс к теме

        Args:
            res: Ресурс для добавления
        """
        self.resources.append(res)

    def add_note(self,note:Note) -> None:
        """
        Добавляет заметку к теме

        Args:
            note: Заметка для добавления
        """
        self.notes.append(note)


    def add_progress(self,entry:ProgressEntry) -> None:
        """
        Добавляет запись о прогрессе
        
        Args:
            entry: запись прогресса
        """
        self.progress.append(entry)


    def to_dict(self) -> Dict:
        """
        Возвращает словарь для сериализации в JSON

        Returns:
            Словарь с данными темы
        """

        return {
            "title":self.title,
            "description":self.description,
            "resources":[r.to_dict() for r in self.resources],
            "notes": [n.to_dict() for n in self.notes],
            "progress": [p.to_dict() for p in self.progress],
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> Topic:
        """
        Создает тему из словаря JSON.

        Args:
            data: Словарь с данными темы

        Returns:
            Экземпляр класс Topic
        """
        from models.resource import Resource
        from models.note import Note
        from models.progress import ProgressEntry

        topic = cls(data["title"], data.get("description",""))
        topic.resources = [Resource.from_dict(r) for r in data.get("resources",[])]
        topic.notes = [Note.from_dict(n) for n in data.get("notes",[])]
        topic.progress = [ProgressEntry.from_dict(p) for p in data.get("progress",[])]
        return topic
    
    def __str__(self) -> str:
        """строковое представление темы."""
        return f"Topic({self.title})"


