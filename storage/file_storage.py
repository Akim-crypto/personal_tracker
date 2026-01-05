"""
Модуль для работы с JSON-файлом хранения данных.
Реализует автосохранение через менеджер контекста.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator

import json

from models.user import User


class FileStorage:
    """
    Класс для работы с JSON-файлом данных трекера.

    Хранит данные в памяти (self._data) и умеет сохранять/загружать JSON.
    """

    def __init__(self, filepath: str = "data/data.json"):
        """
        Инициализация хранилища.

        Args:
            filepath: Путь к JSON-файлу (по умолчанию data/data.json).
        """
        self.filepath: Path = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Any] = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """
        Загружает данные из JSON-файла.

        Returns:
            Словарь с данными или пустой словарь, если файла нет/он поврежден.
        """
        if not self.filepath.exists():
            return {}

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_data(self) -> None:
        """Сохраняет текущие данные self._data в JSON-файл."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get_user(self) -> User | None:
        """
        Возвращает текущего пользователя.

        Returns:
            Экземпляр User или None, если пользователь ещё не создан.
        """
        user_data = self._data.get("user")
        return User.from_dict(user_data) if user_data else None

    def create_user(self, username: str) -> User:
        """
        Создает нового пользователя и сразу сохраняет.

        Args:
            username: Имя пользователя.

        Returns:
            Созданный пользователь.
        """
        user = User(username)
        self._data["user"] = user.to_dict()
        self._save_data()
        return user

    def update_user(self, user: User) -> None:
        """
        Записывает текущее состояние пользователя в self._data и сохраняет.

        Args:
            user: Пользователь с обновлёнными данными.
        """
        self._data["user"] = user.to_dict()
        self._save_data()

    @contextmanager
    def session(self) -> Iterator[User]:
        """
        Контекст “сессии” для изменения пользователя с автосохранением.

        На входе возвращает объект User (создаст, если его ещё нет).
        На выходе автоматически сохраняет изменения.

        Yields:
            User: объект пользователя для изменения.
        """
        user = self.get_user()
        if user is None:
            user = self.create_user("default")

        try:
            yield user
        finally:
            self.update_user(user)

    def __str__(self) -> str:
        """Строковое представление хранилища."""
        return f"FileStorage({self.filepath})"
