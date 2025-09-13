import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def setup_category(client: TestClient):
    """Автоматически создаем категорию для тестов товаров"""
    category_data = {"name": "Электроника", "parent_id": None}
    client.post("/api/v1/category/create", json=category_data)


def test_create_product(client: TestClient, sample_product_data):
    """Тест создания товара"""
    response = client.post("/api/v1/products/create", json=sample_product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status_code"] == 201
    assert data["transaction"] == "Successful"


def test_create_product_invalid_category(client: TestClient):
    """Тест создания товара с несуществующей категорией"""
    product_data = {
        "name": "Тестовый товар",
        "description": "Описание",
        "price": 1000,
        "image_url": "https://example.com/image.jpg",
        "stock": 5,
        "category": 999
    }
    response = client.post("/api/v1/products/create", json=product_data)
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


def test_get_all_products(client: TestClient, sample_product_data):
    """Тест получения всех товаров"""
    # Создаем товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Получаем все товары
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_product_data["name"]


def test_get_products_by_category(client: TestClient, sample_product_data):
    """Тест получения товаров по категории"""
    # Создаем товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Получаем товары по категории
    response = client.get("/api/v1/products/category/elektronika")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_product_data["name"]


def test_get_product_detail(client: TestClient, sample_product_data):
    """Тест получения деталей товара"""
    # Создаем товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Получаем детали товара
    response = client.get("/api/v1/products/detail/iphone-15")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_product_data["name"]


def test_update_product(client: TestClient, sample_product_data):
    """Тест обновления товара"""
    # Создаем товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Обновляем товар
    update_data = {"name": "iPhone 15 Pro", "price": 109900}
    response = client.put("/api/v1/products/detail/iphone-15", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["transaction"] == "Product update is successful"


def test_delete_product(client: TestClient, sample_product_data):
    """Тест удаления товара"""
    # Создаем товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Удаляем товар
    response = client.delete("/api/v1/products/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction"] == "Product delete is successful"


def test_create_product_duplicate_name(client: TestClient, sample_product_data):
    """Тест создания товара с дублирующимся названием"""
    # Создаем первый товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Пытаемся создать второй с тем же названием
    response = client.post("/api/v1/products/create", json=sample_product_data)
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_get_products_pagination(client: TestClient, sample_product_data):
    """Тест пагинации товаров"""
    # Создаем товар
    client.post("/api/v1/products/create", json=sample_product_data)
    
    # Тестируем пагинацию
    response = client.get("/api/v1/products/?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_product_validation(client: TestClient):
    """Тест валидации данных товара"""
    # Тест с пустым названием
    invalid_data = {
        "name": "",
        "description": "Описание",
        "price": 1000,
        "image_url": "https://example.com/image.jpg",
        "stock": 5,
        "category": 1
    }
    response = client.post("/api/v1/products/create", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_product_negative_price(client: TestClient):
    """Тест с отрицательной ценой"""
    invalid_data = {
        "name": "Товар",
        "description": "Описание",
        "price": -100,
        "image_url": "https://example.com/image.jpg",
        "stock": 5,
        "category": 1
    }
    response = client.post("/api/v1/products/create", json=invalid_data)
    assert response.status_code == 422  # Validation error
