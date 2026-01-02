"""
модуль для работы с пользователем в трекере прогресса
"""


from __future__ import annotations
from typing import List,Dict
from models.topic import Topic

class User:
    """
    Класс пользователя трекера прогресса.

    Содержит имя пользователя и список тем для изучения.
    """
    def __init__(self,username:str):
        """
        Инициализация пользователя.

        Args:
            username: Имя пользователя
            """
        self.username = username
        self.topics: List[Topic] = []

    def add_topic(self,topic:Topic) -> None:
        """
        Добавляет тему к пользователю.

        Args:
            topic: Тема для добавления
        """
        self.topics.append(topic)

    def to_dict(self) -> Dict:
        """
        Возвращает словарь для сериализации в JSON.

        Returns:
            Словарь с данными пользователя
        """
        return {
            "username":self.username,
            "topics": [t.to_dict() for t in self.topics],
        }
    
    @classmethod
    def from_dict(cls,data: Dict) -> User:
        """
        Создает пользователя из словаря JSON.

        Args:
            data: Словарь с данными пользователя

        Returns:
            Экземпляр класса User
        """
        user = cls(data["username"])
        user.topics = [Topic.from_dict(t) for t in data.get("topics",[])]
        return user
    
    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"User({self.username})"
    