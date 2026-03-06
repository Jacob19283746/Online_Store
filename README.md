# Online Store API

Production-ready REST API для интернет-магазина, построенное на FastAPI с использованием SQLAlchemy и SQLite.

## Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/Jacob19283746/Online_Store.git
cd Online_Store

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate для Windows

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
alembic upgrade head

# Запуск приложения
uvicorn app.main:app --reload
```

API будет доступно по адресу: `http://localhost:8000`

## Документация

После запуска приложения документация API доступна по следующим адресам:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Архитектура

Проект следует принципам чистой архитектуры и разделения ответственности:

```
Online_Store/
├── app/
│   ├── main.py                 # Точка входа приложения
│   ├── schemas.py              # Pydantic схемы для валидации
│   ├── backend/
│   │   ├── db.py               # Конфигурация базы данных
│   │   └── db_depends.py       # Зависимости для работы с БД
│   ├── models/                 # SQLAlchemy модели
│   │   ├── category.py
│   │   └── products.py
│   ├── routers/                # API эндпоинты
│   │   ├── category.py
│   │   └── products.py
│   └── migrations/             # Alembic миграции
├── tests/                      # Тесты
├── requirements.txt
├── alembic.ini
└── README.md
```

## Технологический стек

- **Python 3.11+**
- **FastAPI 0.115.0** - современный веб-фреймворк
- **SQLAlchemy 2.0.35** - ORM для работы с БД
- **Pydantic 2.9.2** - валидация данных
- **Alembic** - система миграций
- **SQLite** - база данных (легко заменить на PostgreSQL)
- **Uvicorn** - ASGI сервер

## API Эндпоинты

### Товары

| Метод    | Эндпоинт                                     | Описание                                    |
|----------|----------------------------------------------|---------------------------------------------|
| `GET`    | `/api/v1/products/`                          | Получить все активные товары (с пагинацией) |
| `POST`   | `/api/v1/products/create`                    | Создать новый товар                         |
| `GET`    | `/api/v1/products/category/{category_slug}`  | Получить товары по категории                |
| `GET`    | `/api/v1/products/detail/{product_slug}`     | Получить детали товара                      |
| `PUT`    | `/api/v1/products/detail/{product_slug}`     | Обновить товар                              |
| `DELETE` | `/api/v1/products/delete/{product_id}`       | Мягкое удаление товара                      |

### Категории

| Метод    | Эндпоинт                                | Описание                        |
|----------|-----------------------------------------|---------------------------------|
| `POST`   | `/api/v1/category/create`               | Создать новую категорию         |
| `GET`    | `/api/v1/category/all_categories`       | Получить все активные категории |
| `GET`    | `/api/v1/category/{category_id}`        | Получить категорию по ID        |
| `GET`    | `/api/v1/category/slug/{category_slug}` | Получить категорию по slug      |
| `PUT`    | `/api/v1/category/update/{category_id}` | Обновить категорию              |
| `DELETE` | `/api/v1/category/delete/{category_id}` | Мягкое удаление категории       |

## Тестирование

Проект включает полный набор тестов с покрытием основных сценариев:

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного теста
pytest tests/test_products.py::test_create_product
```

## Миграции базы данных

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## Развертывание

### Локальная разработка

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Продакшн

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Для продакшн окружения рекомендуется:
- Использовать PostgreSQL вместо SQLite
- Настроить переменные окружения для конфигурации
- Использовать reverse proxy (nginx)
- Настроить мониторинг и логирование

## Основные возможности

- Полный CRUD для товаров и категорий
- Иерархическая структура категорий
- Мягкое удаление (soft delete)
- Валидация данных с Pydantic
- Автоматическая документация API
- Пагинация для списков
- Обработка ошибок
- CORS поддержка

## Примеры использования

### Создание категории

```bash
curl -X POST "http://localhost:8000/api/v1/category/create" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Электроника",
       "parent_id": null
     }'
```

### Создание товара

```bash
curl -X POST "http://localhost:8000/api/v1/products/create" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "iPhone 15",
       "description": "Новейший смартфон от Apple",
       "price": 99900,
       "image_url": "https://example.com/iphone15.jpg",
       "stock": 10,
       "category": 1
     }'
```

## Автор 
- #### [Jacob Grigorev](https://github.com/Jacob19283746/)

