import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.backend.db import Base
from app.backend.db_depends import get_db

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределяем зависимость для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def setup_database():
    """Создаем тестовую базу данных для каждого теста"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_database):
    """Создаем тестовый клиент"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_category_data():
    """Тестовые данные для категории"""
    return {
        "name": "Электроника",
        "parent_id": None
    }


@pytest.fixture
def sample_product_data():
    """Тестовые данные для товара"""
    return {
        "name": "iPhone 15",
        "description": "Новейший смартфон от Apple",
        "price": 99900,
        "image_url": "https://example.com/iphone15.jpg",
        "stock": 10,
        "category": 1
    }
