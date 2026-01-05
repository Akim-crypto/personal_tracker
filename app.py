"""
CLI-приложение "Персональный трекер прогресса и база знаний".

Возможности:
- Создание пользователя (если не существует).
- Управление темами: добавление, просмотр.
- Добавление ресурсов, заметок и прогресса к теме.
- Сохранение в JSON через FileStorage (автосохранение в конце session()).
"""

from __future__ import annotations

from typing import Callable

from core.utils import validate_url, find_topic_by_title
from models.note import Note
from models.progress import ProgressEntry
from models.resource import  Resource
from models.topic import Topic
from storage.file_storage import FileStorage

def _input_non_empty(promt:str) -> str:
    """Запрашивает непустую строку у пользователя
    
    Args
        promt: Текст приглашения

    Returns
        непустая строка
    """

    while True:
        value = input(promt).strip()
        if value:
            return value
        print("Введите непустое значение")

def _input_int(promt: str , * , min_value:int | None = None , max_value:
               int | None = None) -> int:
    """
    Запрашивает целое число с валидацией диапазона
    
    Args:
    promt: Текст приглашения
    min_value минимально допустимое значение (включительно)
    max_value максимально допустимое значение

    Returns
        Введенное целое число
    """

    while True:
        raw = input(promt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Введите целое число")
            continue

        if min_value is not None and value < min_value:
            print(f"Число должно быть >= {min_value}")
            continue

        if max_value is not None and value > max_value:
            print(f"Число должно быть <= {max_value}")
            continue

        return value
    

def _chose_topic(user) -> Topic | None:
    """Просит выбрать тему по названию
        
        Args
            user Экземпляр User

        Returns
            Найденная тема или None
    """

    if not user.topics:
        print("Тем пока нет. Сначала добавьте тему")
        return None
    
    print("Существующие темы:")
    for i , t in enumerate(user.topics , start=1):
        print(f"{i}. {t.title}")

        title = _input_non_empty("Введите точное название темы")
        topic = find_topic_by_title(user,title)
        if topic is None:
            print("Тема не найдена")
        return topic

def cmd_show_user(storage: FileStorage) -> None:
    """Показывает пользователя и краткую статистику"""
    with storage.session() as user:
        print(f"Пользователь. {user.username}")
        print(f"Тем: {len(user.topics)}")


def cmd_set_username(storage:FileStorage) -> None:
    """Меняет имя пользователя"""
    with storage.session() as user:
        username = _input_non_empty("Введите новое имя пользователя")
        user.username = username
        print("Имя обновлено")


def cmd_add_topic(storage:FileStorage) -> None:
    """Добавляет новую тему"""
    with storage.session() as user:
        title = _input_non_empty("Название темы")
        if find_topic_by_title(user,title) is not None:
            print("Такая тема уже есть")
            return
        
        description = input("Описание (можно пустое):").strip()
        user.add_topic(Topic(title=title , description=description))
        print("Тема добавлена")


def cmd_list_topics(storage: FileStorage) -> None:
    """Показывает все темы"""
    with storage.session() as user:
        if not user.topics:
            print("Тем пока нет")
            return
        
        for i , t in enumerate(user.topics,start=1):
            print(f"{i}. {t.title} - {t.description}")


def cmd_add_resource(storage: FileStorage) -> None:
    """Добавляет ресурс (link/text) к выбранной теме"""
    with storage.session() as user:
        topic = _chose_topic(user)
        if topic is None:
            return
        
        res_type = _input_non_empty("Тип ресурса (link/text):").lower()
        if res_type not in {"link" , "text"}:
            print("Поддерживаются только 'link' и 'text'")
            return
        
        content = _input_non_empty("Содержимое (URL или текст)")
        if res_type == "link" and not validate_url(content):
            print("URL не прошел валидацию")
            return
        
        topic.add_resource(Resource(res_type=res_type,content=content))
        print("Ресурс добавлен")


def cmd_add_note(storage:FileStorage) -> None:
    """добавляет заметку к выбранной теме"""
    with storage.session() as user:
        topic = _chose_topic(user)
        if topic is None:
            return
        
        text = _input_non_empty("Текст заметки:")
        topic.add_note(Note(text=text))
        print("Заметка добавлена")

def cmd_update_progress(storage:FileStorage) -> None:
    """Добавляет запись прогресса (0..100) к выбранной теме"""
    with storage.session() as user:
        topic = _chose_topic(user)
        if topic is None:
            return
        
        percent = _input_int("Процент прогресса (0-100):" , min_value=0,
                max_value=100)
        topic.add_progress(ProgressEntry(percent=percent))
        print("Прогресс обновлен")


def cmd_show_topic_details(strorage:FileStorage) -> None:
    """показывает детали выбранной темы"""
    with strorage.session() as user:
        topic = _chose_topic(user)
        if topic is None:
            return
        
        print(f"Тема: {topic.title}")
        print(f"Описание: {topic.description}")

        print("\nРесурсы")
        if topic.resources:
            for r in topic.resources:
                print(f"- {r}")
        else:
            print("- (пусто)")

        print("\nЗаметки:")
        if topic.notes:
            for n in topic.notes:
                print(f"- {n}")
        else:
            print("- (пусто)")

        print("\nПрогресс:")
        if topic.progress:
            for p in topic.progress:
                print(f"- {p}")
        else:
            print("- (пусто)")   

def ensure_user_exists(storage: FileStorage) -> None:
    """
    Гарантирует наличие пользователя в хранилище.
    Если пользователя нет — создаёт (спросив имя).
    """
    user = storage.get_user()
    if user is not None:
        return

    username = _input_non_empty("Пользователь не найден. Введите имя пользователя: ")
    storage.create_user(username)


def main() -> None:
    """Точка входа CLI."""
    storage = FileStorage("data/data.json")
    ensure_user_exists(storage)

    actions: dict[str, tuple[str, Callable[[FileStorage], None]]] = {
        "1": ("Показать пользователя", cmd_show_user),
        "2": ("Сменить имя пользователя", cmd_set_username),
        "3": ("Добавить тему", cmd_add_topic),
        "4": ("Список тем", cmd_list_topics),
        "5": ("Добавить ресурс в тему", cmd_add_resource),
        "6": ("Добавить заметку в тему", cmd_add_note),
        "7": ("Обновить прогресс по теме", cmd_update_progress),
        "8": ("Показать детали темы", cmd_show_topic_details),
        "0": ("Выход", lambda _: None),
    }

    while True:
        print("\n=== Персональный трекер прогресса ===")
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")

        choice = input("Выберите пункт: ").strip()
        if choice == "0":
            print("Выход.")
            break

        action = actions.get(choice)
        if action is None:
            print("Неверный пункт меню.")
            continue

        _, fn = action
        fn(storage)


if __name__ == "__main__":
    main()