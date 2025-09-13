import pytest
from fastapi.testclient import TestClient


def test_welcome(client: TestClient):
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_health_check(client: TestClient):
    """Тест проверки здоровья API"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_404_handler(client: TestClient):
    """Тест обработчика 404 ошибок"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "available_endpoints" in data
