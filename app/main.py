from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import category, products
import uvicorn

# Создание экземпляра FastAPI с метаданными
app = FastAPI(
    title="🛒 Online Store API",
    description="""
    Современное REST API для интернет-магазина.
    
    ## Особенности
    
    * **Товары** - полный CRUD для управления товарами
    * **Категории** - иерархическая структура категорий
    * **Валидация** - строгая валидация данных с Pydantic
    * **Документация** - автоматическая генерация OpenAPI/Swagger
    
    ## Технологии
    
    * FastAPI
    * SQLAlchemy
    * SQLite
    * Alembic
    """,
    version="1.0.0",
    contact={
        "name": "Developer",
        "email": "developer@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Главная"])
async def welcome() -> dict:
    """
    Приветственное сообщение API
    """
    return {
        "message": "Добро пожаловать в Online Store API!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Система"])
async def health_check() -> dict:
    """
    Проверка состояния API
    """
    return {
        "status": "healthy",
        "message": "API работает корректно"
    }


# Подключение роутеров
app.include_router(category.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")


# Обработчик исключений
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "detail": "Endpoint not found",
        "status_code": 404,
        "available_endpoints": [
            "/docs",
            "/redoc", 
            "/api/v1/category/",
            "/api/v1/products/"
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
