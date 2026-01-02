"""
Модуль для работы с ресурсами (ссылки тексты)
"""

from __future__ import annotations
from typing import Dict

class Resource:
    """
    Базовый класс для ресурсов темы

    Поддерживает ссылки тексты и другие типы ресурсов
    """

    def __init__(self,res_type:str , content:str):
        """
        Инициализация ресурса

        Args:
            res_type: Тип ресурса ('link','text',etc)
            content содержимое ресурса
        """
        self.res_type = res_type
        self.content = content

    def to_dict(self) -> Dict:
        """Возвращает словарь для сериализации в JSON
        
        Return
            Словарь с данными ресурса
        """

        return {"type":self.res_type , "content":self.content}
    
    @classmethod
    def from_dict(cls , data:Dict) -> Resource:
        """
        Создает ресурс из словаря JSON

        Args:
            data: словарь с данными ресурса

        Returns:
            Экземпляр класса Resource
        """
        return cls(data["type"],data["content"])
    
    def __str__(self) -> str:
        """
        Строковое представление ресурса
        """

        return f"[{self.res_type}] {self.content}"
    

