"""
ФИНАЛЬНЫЕ тесты CLI — работают стабильно.
"""

import io
import sys
from pathlib import Path
from unittest.mock import patch
import pytest
from models.topic import Topic
from storage.file_storage import FileStorage


@pytest.fixture(autouse=True)
def clean_data():
    """Очищает data/data.json."""
    path = Path("data/data.json")
    if path.exists():
        path.unlink()
    yield
    if path.exists():
        path.unlink()


class MockStdin:
    """Правильная подмена sys.stdin.readline()."""
    def __init__(self, inputs):
        self.inputs = iter(inputs)
    
    def readline(self):
        try:
            return next(self.inputs) + '\n'
        except StopIteration:
            return '\n'


def test_app_show_user(capsys):
    """Показать пользователя."""
    inputs = ["test_user", "1", "0"]
    
    with patch('sys.stdin', MockStdin(inputs)):
        from app import main
        main()
    
    captured = capsys.readouterr()
    assert "Пользователь: test_user" in captured.out


def test_app_add_topic(capsys):
    """Добавить тему."""
    inputs = ["test_user", "3", "Python OOP", "Основы ООП", "4", "0"]
    
    with patch('sys.stdin', MockStdin(inputs)):
        from app import main
        main()
    
    storage = FileStorage()
    with storage.session() as user:
        assert len(user.topics) == 1
        assert user.topics[0].title == "Python OOP"


def test_app_add_resource(capsys):
    """Добавить ресурс."""
    # 1. Создаём тему
    inputs1 = ["test_user", "3", "Test Topic", "", "0"]
    with patch('sys.stdin', MockStdin(inputs1)):
        from app import main
        main()
    
    # 2. Добавляем ресурс
    inputs2 = ["5", "Test Topic", "link", "https://example.com", "0"]
    with patch('sys.stdin', MockStdin(inputs2)):
        from app import main
        main()
    
    storage = FileStorage()
    with storage.session() as user:
        topic = next(t for t in user.topics)
        assert len(topic.resources) == 1


def test_app_invalid_choice(capsys):
    """Неверный выбор."""
    inputs = ["test_user", "9", "0"]
    
    with patch('sys.stdin', MockStdin(inputs)):
        from app import main
        main()
    
    captured = capsys.readouterr()
    assert "Неверный пункт меню." in captured.out


def test_app_list_empty_topics(capsys):
    """Пустой список тем."""
    inputs = ["test_user", "4", "0"]
    
    with patch('sys.stdin', MockStdin(inputs)):
        from app import main
        main()
    
    captured = capsys.readouterr()
    assert "Тем пока нет." in captured.out


def test_app_ensure_user_exists(capsys):
    """Создание пользователя."""
    inputs = ["test_new_user", "1", "0"]
    
    with patch('sys.stdin', MockStdin(inputs)):
        from app import main
        main()
    
    storage = FileStorage()
    assert storage.get_user().username == "test_new_user"
