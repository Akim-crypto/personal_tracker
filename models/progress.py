"""
Модуль для отслеживания прогресса по темам.
"""

from __future__ import annotations
from typing import Dict
from datetime import datetime


class ProgressEntry:
    """
    Класс записи о прогрессе по теме.

    Содержит процент выполнения и дату записи.
    """

    def __init__(self, percent: int, date: str | None = None):
        """
        Инициализация записи прогресса.

        Args:
            percent: Процент выполнения (0-100)
            date: Дата записи (ISO формат, опционально)
        """
        self.percent = percent
        self.date = date or datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> Dict:
        """
        Возвращает словарь для сериализации в JSON.

        Returns:
            Словарь с данными записи прогресса
        """
        return {"percent": self.percent, "date": self.date}

    @classmethod
    def from_dict(cls, data: Dict) -> ProgressEntry:
        """
        Создает запись прогресса из словаря JSON.

        Args:
            data: Словарь с данными записи прогресса

        Returns:
            Экземпляр класса ProgressEntry
        """
        return cls(data["percent"], data["date"])

    def __str__(self) -> str:
        """Строковое представление записи прогресса."""
        return f"{self.date}: {self.percent}%"
