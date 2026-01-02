"""
Модуль для работы с заметками
"""

from __future__ import annotations
from typing import Dict
from datetime import datetime

class Note:
    """
    Класс заметки для темы

    Содержит текст заметки и время создания
    """

    def __init__(self,text:str,created_at:str | None = None):
        """
        Инициализация заметки

        Args:
            text: Текст заметки
            created_at : Время создания (ISO опционально)
        """

        self.text = text
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")


    def to_dict(self) -> Dict:
        """
        Возвращает словарь для сериализации в JSON

        Returns:
            Словарь с данными заметки
        """

        @classmethod
        def from_dict(cls,data:Dict) -> None:
            """
            Создает заметку из словаря JSON
            
            Args:
                data: словарь с данными заметки

            Returns:
                Экземпляр класса Note    
            """
            return cls(data["text"] , data["created_at"])
        
        def __str__(self) -> str:
            """строковое представление заметки"""
            return f"{self.created_at}: {self.text}"