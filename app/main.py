from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import category, products
import uvicorn


app = FastAPI(
    title="Store API",
    description="""
    Современное REST API для интернет-магазина.
    
    Особенности:
    
    * Товары - полный CRUD для управления товарами
    * Категории - иерархическая структура категорий
    * Валидация - строгая валидация данных с Pydantic
    * Документация - автоматическая генерация OpenAPI/Swagger
    
    Технологии:
    
    * FastAPI
    * SQLAlchemy
    * SQLite
    * Alembic
    """,
    version="1.0.0",
    contact={
        "name": "Jacob Grigorev",
        "email": "grigorevakov2001@outlook.com",
    },
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "message": "Добро пожаловать в Store API!",
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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Обработчик для маршрутных 404 ошибок (не для HTTPException из роутеров)"""
    if exc.status_code == 404:
        detail = getattr(exc, 'detail', '')
        if detail in ('Not Found', '', None) or 'not found' in str(detail).lower():
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "Endpoint not found",
                    "status_code": 404,
                    "available_endpoints": [
                        "/docs",
                        "/redoc", 
                        "/api/v1/category/",
                        "/api/v1/products/"
                    ]
                }
            )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail} if hasattr(exc, 'detail') else {"detail": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
