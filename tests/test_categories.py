import pytest
from fastapi.testclient import TestClient


def test_create_category(client: TestClient, sample_category_data):
    """Тест создания категории"""
    response = client.post("/api/v1/category/create", json=sample_category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status_code"] == 201
    assert data["transaction"] == "Successful"


def test_create_category_duplicate_name(client: TestClient, sample_category_data):
    """Тест создания категории с дублирующимся названием"""
    # Создаем первую категорию
    client.post("/api/v1/category/create", json=sample_category_data)
    
    # Пытаемся создать вторую с тем же названием
    response = client.post("/api/v1/category/create", json=sample_category_data)
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_get_all_categories(client: TestClient, sample_category_data):
    """Тест получения всех категорий"""
    # Создаем категорию
    client.post("/api/v1/category/create", json=sample_category_data)
    
    # Получаем все категории
    response = client.get("/api/v1/category/all_categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_category_data["name"]


def test_get_category_by_id(client: TestClient, sample_category_data):
    """Тест получения категории по ID"""
    # Создаем категорию
    client.post("/api/v1/category/create", json=sample_category_data)
    
    # Получаем категорию по ID
    response = client.get("/api/v1/category/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_category_data["name"]


def test_get_category_by_slug(client: TestClient, sample_category_data):
    """Тест получения категории по slug"""
    # Создаем категорию
    client.post("/api/v1/category/create", json=sample_category_data)
    
    # Получаем категорию по slug
    response = client.get("/api/v1/category/slug/elektronika")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_category_data["name"]


def test_update_category(client: TestClient, sample_category_data):
    """Тест обновления категории"""
    # Создаем категорию
    client.post("/api/v1/category/create", json=sample_category_data)
    
    # Обновляем категорию
    update_data = {"name": "Обновленная электроника"}
    response = client.put("/api/v1/category/update/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["transaction"] == "Category update is successful"


def test_delete_category(client: TestClient, sample_category_data):
    """Тест удаления категории"""
    # Создаем категорию
    client.post("/api/v1/category/create", json=sample_category_data)
    
    # Удаляем категорию
    response = client.delete("/api/v1/category/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction"] == "Category delete is successful"


def test_create_category_with_invalid_parent(client: TestClient):
    """Тест создания категории с несуществующим родителем"""
    data = {
        "name": "Подкатегория",
        "parent_id": 999
    }
    response = client.post("/api/v1/category/create", json=data)
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]
