Personal Progress Tracker & Knowledge Base
Персональный трекер прогресса и база знаний — это учебный проект, который помогает структурировать обучение и параллельно прокачивать навыки Python, ООП, работы с файлами, тестирования, FastAPI и SQLAlchemy.

Проект развивается по этапам:

консольное приложение с JSON‑хранилищем,

веб‑API на FastAPI,

переход на полноценную БД (SQLite/SQLAlchemy), а дальше — расширение (аутентификация, асинхронность, Docker и т.д.).

Возможности
Этап 1 — CLI‑приложение
Ведение тем для изучения (например, “Основы Python”, “Базы данных”).

Добавление к темам:

ресурсов (ссылки, текстовые материалы),

заметок,

записей о прогрессе (проценты выполнения).

Хранение данных в JSON‑файле:

безопасная работа с файлами через with open(...),

сериализация моделей в dict и обратно.

Удобное консольное меню:

показать пользователя и количество тем,

добавление/просмотр тем,

добавление ресурса/заметки/прогресса к конкретной теме.

Этап 2 — FastAPI‑API
REST API для работы с темами:

GET /health — статус сервиса,

GET /topics — список тем,

POST /topics — создание новой темы,

GET /topics/{title} — получение темы по названию.

Pydantic‑схемы для валидации запросов и формирование ответов.

Переход от файлового хранилища к SQLite + SQLAlchemy для сущности Topic (и дальше — расширение на ресурсы/заметки/прогресс).

Архитектура и стек
Стек технологий
Язык: Python 3.12

CLI: стандартная библиотека (input, print, json, pathlib)

Веб‑часть: FastAPI

Хранилище:

Этап 1: JSON‑файл (data/data.json)

Этап 2: SQLite (data/tracker.db) + SQLAlchemy (ORM)

Тестирование: pytest

Типизация: аннотации типов, from __future__ import annotations

Структура проекта (упрощённо)
text
personal_tracker/
├── app/
│   ├── api/
│   │   └── topics.py        # FastAPI роуты для тем
│   ├── db/
│   │   ├── database.py      # engine, SessionLocal, Base, get_db()
│   │   ├── init_db.py       # создание таблиц
│   │   └── models.py        # ORM-модели (TopicModel и др.)
│   ├── schemas/
│   │   └── topic.py         # Pydantic-схемы для API
│   ├── services/
│   │   └── topic_service.py # CRUD-логика для тем
│   └── main.py              # FastAPI приложение
├── core/
│   └── utils.py             # валидация URL, поиск тем и т.п.
├── models/
│   ├── user.py              # User (CLI-модель)
│   ├── topic.py             # Topic + ресурсы/заметки/прогресс (CLI)
│   ├── resource.py
│   ├── note.py
│   └── progress.py
├── storage/
│   └── file_storage.py      # JSON-хранилище с автосохранением
├── tests/
│   ├── test_storage.py      # тесты хранилища
│   ├── test_app.py          # тесты CLI
│   └── ...                  # (дальше — тесты для FastAPI)
├── data/
│   ├── data.json            # данные для CLI
│   └── tracker.db           # SQLite БД для FastAPI/ORM
└── app.py                   # CLI-приложение
Ключевые технические идеи
Объектно‑Ориентированная модель
Модели уровня домена (CLI):

User — пользователь и его список тем.

Topic — тема изучения.

Resource — ресурс (ссылка/текст).

Note — заметка.

ProgressEntry — запись прогресса.

У каждой модели:

to_dict() / from_dict() для сериализации в JSON,

__str__() для человекочитаемого вывода.

Файловое хранилище с менеджером контекста
FileStorage отвечает за:

загрузку данных из JSON при создании,

сохранение данных в JSON,

предоставление контекста session():

python
with storage.session() as user:
    user.add_topic(topic)
    # при выходе изменения автоматически сохраняются
Переход к FastAPI и SQLite
Pydantic‑схемы:

TopicCreate, TopicRead, ResourceCreate, NoteCreate, ProgressCreate.

FastAPI:

отдельный роутер topics.py,

зависимость get_db() для работы с SQLAlchemy‑сессией.

SQLAlchemy:

TopicModel как ORM‑модель таблицы topics,

сервисный слой topic_service.py для CRUD‑операций.

Запуск проекта
1. Установка зависимостей
Создай виртуальное окружение и установи необходимые пакеты:

bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# или
.venv\Scripts\activate          # Windows

pip install fastapi uvicorn sqlalchemy pydantic pytest
(При необходимости можно вынести зависимости в requirements.txt или перейти на Poetry.)

2. CLI‑приложение (Этап 1)
bash
python app.py
Пример сценария:

Ввести имя пользователя.

Добавить тему “Основы Python”.

Добавить к теме ссылку/текстовый ресурс.

Добавить заметку.

Добавить запись о прогрессе (например, 30%).

Все данные сохранятся в data/data.json.

3. FastAPI‑приложение (Этап 2)
bash
uvicorn app.main:app --reload
Доступные точки входа:

Swagger UI: http://127.0.0.1:8000/docs

Проверка здоровья: GET /health

Работа с темами:

GET /topics

POST /topics

GET /topics/{title}

Тестирование
Запуск всех тестов:

bash
pytest -v
В проекте уже покрыты:

модели и файловое хранилище (tests/test_storage.py),

CLI (через подмену sys.stdin и захват вывода),

далее можно добавить тесты для FastAPI (через TestClient).

Дальнейшее развитие
Идеи для следующих этапов:

Перенос ресурсов, заметок и прогресса в БД:

отдельные ORM‑модели и связи One-to-Many с TopicModel.

Добавление пользователей и аутентификации (JWT).

Асинхронный FastAPI + асинхронный драйвер БД.

Документация:

автогенерация с помощью Sphinx или MkDocs по докстрингам.

Код‑стайл и качество:

интеграция ruff, black, mypy, pre-commit хуков.

Docker‑контейнеризация:

Dockerfile, docker-compose.yml для быстрой развёртки.