from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from typing import Generator


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass


# Получаем URL базы данных из переменной окружения или используем значение по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Создаем движок базы данных
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False").lower() == "true",  # Логирование SQL запросов в режиме отладки
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Генератор для получения сессии базы данных
    
    Yields:
        Session: Сессия SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Удаляет все таблицы из базы данных"""
    Base.metadata.drop_all(bind=engine)
