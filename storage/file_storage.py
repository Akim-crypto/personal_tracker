"""
Модуль для работы с JSON-файлом хранения данных
Реализует автосохранение через менеджер контекста
"""

from __future__ import annotations
from typing import Dict,Any
from contextlib import contextmanager
import json
import os
from pathlib import Path
from models.user import User

class FileStorage:
    """
    Класс для работы с JSON-файлом данных трекера
    Автоматически сохраняет изменения при выходе из контекста
    """

    def __init__(self,filepath: str = "data/data.json"):
        """
        Инициализация хранилища
        
        Args:
            filepath: Путь к json файлу (по умолчанию data/data.json)
        """
        self.filepath: Path = Path(filepath)
        self.filepath.parent.mkdir(parents=True,exist_ok=True)
        self._data: Dict[str,Any] = self._load_data()

    def _load_data(self) -> Dict[str,Any]:
        """
        Загружает данные из JSON-файла
        
        Returns
            словарь с данными или пустой словарь
        """

        if self.filepath.exists():
            try:
                with open(self.filepath,"r",encoding="utf-8") as f :
                    return json.load(f)
            except (json.JSONDecodeError,IOError):
                print("❌ файл поврежден создаю новый")
        return {}
    
    def _save_data(self) -> None:
        """
        Сохраняет данные в JSON файл
        """
        try:
            with open(self.filepath, "w" , encoding="utf-8")as f :
                json.dump(self._data, f , ensure_ascii=False , indent=2)
        except IOError as e:
            print(f"❌ ошибка сохранения: {e}")
        
    
    def get_user(self) -> User | None:
        """
        Возвращает текущего пользователя

        Returns
            Экземпляр User или None если пользователь не создан
        """
        user_data = self._data.get("user")
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def create_user(self,username:str) -> User:
        """Создает нового пользователя
        
        Args
            username имя пользователя

        Returns
            Созданный пользователь    
        """
        user = User(username)
        self._data["user"] = user.to_dict()
        self._save_data()
        return user
    
    def update_user(self,user:User) -> None:
        """Обновляет данные пользователя в хранилище
        
        Args
            user: Пользователь с обновленными данными
        """
        self._data["user"] = user.to_dict()
        self._save_data()

    @contextmanager
    def session(self) -> FileStorage:
        """Менеджер контекста
        
        Usage:
            with storage.session()
                user.add_topic(topic)
                # Автосохранение при выходе из контекста
        """

        try:
            yield self
        finally:
            self._save_data()

    def __str__(self) -> str:
        """Строковое представление хранилища"""
        return f"FileStorage{self.filepath}"