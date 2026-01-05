"""
Тесты для модуля storage.
"""

from models.user import User
from models.topic import Topic
from storage.file_storage import FileStorage


def test_create_user():
    """Тест создания пользователя."""
    storage = FileStorage("tests/test_data.json")
    user = storage.create_user("test_user")
    assert user.username == "test_user"
    assert storage.get_user().username == "test_user"

def test_autosave_context():
    """Тест автосохранения через менеджер контекста."""
    storage = FileStorage("tests/test_data.json")

    with storage.session() as user:
        topic = Topic("Python", "Основы")
        user.add_topic(topic)

    reloaded_storage = FileStorage("tests/test_data.json")
    assert len(reloaded_storage.get_user().topics) == 1
