Personal Progress Tracker
Персональный трекер прогресса и база знаний.
Позволяет создавать темы для изучения, добавлять к ним ресурсы, заметки и отслеживать прогресс. Проект сделан как учебный: покрывает ООП, работу с файлами, CLI, FastAPI, SQLAlchemy, pytest и типизацию.

Возможности
Создание пользователя и управление темами

Добавление ресурсов к темам (ссылки и текст)

Добавление заметок

Фиксация прогресса по каждой теме (0–100%)

CLI‑интерфейс для локальной работы

REST API на FastAPI для интеграций и фронтенда

Хранение данных:

Этап 1: JSON‑файл

Этап 2: SQLite + SQLAlchemy (для тем, далее расширяем)

Технологии
Python 3.12

ООП (классы User, Topic, Resource, Note, ProgressEntry)

Работа с файлами (json, with open(...))

Регулярные выражения для валидации URL

FastAPI (REST API, Pydantic‑схемы)

SQLAlchemy + SQLite

pytest (тесты для моделей, хранилища, CLI, API)

Аннотации типов (PEP 484, from __future__ import annotations)

Структура проекта
text
personal_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI приложение
│   ├── api/
│   │   ├── __init__.py
│   │   └── topics.py        # эндпоинты /topics
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py      # engine, SessionLocal, Base, get_db()
│   │   ├── models.py        # ORM-модели (TopicModel и др.)
│   │   └── init_db.py       # init_db()
│   └── schemas/
│       ├── __init__.py
│       └── topic.py         # Pydantic-схемы Topic/Resource/Note/Progress
├── core/
│   ├── __init__.py
│   └── utils.py             # validate_url(), find_topic_by_title()
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── topic.py
│   ├── resource.py
│   ├── note.py
│   └── progress.py
├── storage/
│   ├── __init__.py
│   └── file_storage.py      # FileStorage + context manager
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py       # при необходимости
│   ├── test_storage.py
│   └── test_app.py          # тесты CLI (MockStdin, capsys)
├── data/
│   ├── data.json            # JSON‑хранилище (CLI, промежуточный этап)
│   └── tracker.db           # SQLite база (FastAPI/SQLAlchemy)
└── app.py                   # CLI-приложение
Установка и запуск
1. Клонирование и окружение
bash
git clone <url-репозитория> personal_tracker
cd personal_tracker

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
(Если requirements.txt ещё нет — можно сгенерировать позже через pip freeze.)

2. Запуск CLI
bash
python app.py
Возможности CLI:

Показать пользователя

Сменить имя пользователя

Добавить тему

Показать список тем

Добавить ресурс к теме

Добавить заметку к теме

Обновить прогресс по теме

Показать детали темы

Все изменения сохраняются в data/data.json через FileStorage и контекстный менеджер.

3. Запуск FastAPI
Инициализация базы (создание таблиц):

bash
python -m app.db.init_db
Запуск сервера:

bash
uvicorn app.main:app --reload
Доступные точки:

GET /health — health‑check

GET /topics — список тем

POST /topics — создание темы

GET /topics/{title} — получение темы по названию
(ресурсы/заметки/прогресс на этом этапе ещё в процессе переноса в БД)

Документация:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Тесты
Проект покрыт тестами для:

моделей и сериализации (to_dict/from_dict)

FileStorage (создание пользователя, автосохранение через context manager)

CLI (меню, добавление тем и ресурсов, обработка ошибок ввода)

FastAPI (можно добавить позже TestClient‑тесты)

Запуск тестов:

bash
pytest -v
# или только определённый модуль
pytest tests/test_storage.py -v
pytest tests/test_app.py -v -s
Архитектурные решения
ООП‑модели домена (User, Topic, Resource, Note, ProgressEntry) отделены от инфраструктуры (FileStorage, SQLAlchemy).

FileStorage реализует простой repository поверх JSON‑файла, с автосохранением через контекстный менеджер session().

FastAPI слой использует Pydantic‑схемы для строгой валидации входных данных и удобной автодокументации.

Переход от JSON к SQLite сделан через отдельный слой сервисов (app/services/topic_service.py) и ORM‑модели (TopicModel), что облегчает замену хранилища.

Дальнейшее развитие
Планы на следующие этапы:

Перенос ресурсов, заметок и прогресса в БД (связи один‑ко‑многим)

Асинхронный вариант API (async SQLAlchemy / asyncpg)

Аутентификация пользователей (JWT)

Докеризация (Dockerfile + docker-compose)

mypy + ruff + pre-commit

CI (GitHub Actions) для прогонки тестов и линтинга