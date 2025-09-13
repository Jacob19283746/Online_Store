# 🛒 Online Store API

Современное REST API для интернет-магазина, построенное на FastAPI с использованием SQLAlchemy и SQLite.

## 🚀 Особенности

- **FastAPI** - современный, быстрый веб-фреймворк для создания API
- **SQLAlchemy** - мощная ORM для работы с базой данных
- **Alembic** - система миграций для управления схемой БД
- **Pydantic** - валидация данных и сериализация
- **Иерархические категории** - поддержка вложенных категорий товаров
- **RESTful API** - стандартизированные эндпоинты
- **Автоматическая документация** - Swagger UI и ReDoc

## 📋 Функциональность

### Товары (Products)
- ✅ Получение всех активных товаров
- ✅ Создание нового товара
- ✅ Получение товаров по категории
- ✅ Детальная информация о товаре
- ✅ Обновление товара
- ✅ Мягкое удаление товара

### Категории (Categories)
- ✅ Создание категории
- ✅ Получение всех активных категорий
- ✅ Обновление категории
- ✅ Мягкое удаление категории
- ✅ Поддержка иерархической структуры

## 🛠 Технологический стек

- **Python 3.11+**
- **FastAPI 0.115.0**
- **SQLAlchemy 2.0.35**
- **Pydantic 2.9.2**
- **Alembic** - миграции
- **SQLite** - база данных
- **Uvicorn** - ASGI сервер

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Jacob19283746/Online_Store.git
cd Online_Store
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
alembic upgrade head
```

### 5. Запуск приложения
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

## 📚 API Документация

После запуска приложения документация API доступна по следующим адресам:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🗂 Структура проекта

```
Online_Store/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Точка входа приложения
│   ├── schemas.py              # Pydantic схемы
│   ├── backend/
│   │   ├── db.py              # Конфигурация базы данных
│   │   └── db_depends.py      # Зависимости для работы с БД
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py        # Модель категории
│   │   └── products.py        # Модель товара
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── category.py        # API для категорий
│   │   └── products.py        # API для товаров
│   └── migrations/            # Alembic миграции
├── requirements.txt           # Зависимости Python
├── alembic.ini               # Конфигурация Alembic
└── README.md                 # Документация
```

## 🔧 API Эндпоинты

### Товары
- `GET /products/` - Получить все активные товары
- `POST /products/create` - Создать новый товар
- `GET /products/{category_slug}` - Получить товары по категории
- `GET /products/detail/{product_slug}` - Получить детали товара
- `PUT /products/detail/{product_slug}` - Обновить товар
- `DELETE /products/delete?product_id={id}` - Удалить товар

### Категории
- `POST /category/create` - Создать новую категорию
- `GET /category/all_categories` - Получить все активные категории
- `PUT /category/update_category?category_id={id}` - Обновить категорию
- `DELETE /category/delete?category_id={id}` - Удалить категорию

## 📊 Модели данных

### Product (Товар)
- `id` - Уникальный идентификатор
- `name` - Название товара
- `slug` - URL-дружественное название
- `description` - Описание товара
- `price` - Цена (в копейках)
- `image_url` - URL изображения
- `stock` - Количество на складе
- `category_id` - ID категории
- `rating` - Рейтинг товара
- `is_active` - Активен ли товар

### Category (Категория)
- `id` - Уникальный идентификатор
- `name` - Название категории
- `slug` - URL-дружественное название
- `is_active` - Активна ли категория
- `parent_id` - ID родительской категории (для иерархии)

## 🧪 Примеры использования

### Создание категории
```bash
curl -X POST "http://localhost:8000/category/create" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Электроника",
       "parent_id": null
     }'
```

### Создание товара
```bash
curl -X POST "http://localhost:8000/products/create" \
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

## 🔄 Миграции

Для создания новой миграции:
```bash
alembic revision --autogenerate -m "Описание изменений"
```

Для применения миграций:
```bash
alembic upgrade head
```

## 🚀 Развертывание

### Локальная разработка
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Продакшн
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

