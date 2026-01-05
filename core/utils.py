"""
Утилиты для валидации и работы с данными.
"""

import re
from typing import Optional


def validate_url(url: str) -> bool:
    """
    Проверяет URL с помощью регулярного выражения.

    Args:
        url: Строка URL для проверки

    Returns:
        True, если URL валидный
    """
    pattern = re.compile(
        r'^https?://'  # http:// или https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # домен
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IPv4
        r'(?::\d+)?'  # порт
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def find_topic_by_title(user: 'User', title: str) -> Optional['Topic']:
    """
    Ищет тему по названию (использует list comprehension).

    Args:
        user: Пользователь
        title: Название темы

    Returns:
        Найденная тема или None
    """
    return next((t for t in user.topics if t.title.lower() == title.lower()), None)
