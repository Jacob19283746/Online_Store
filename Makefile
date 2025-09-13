.PHONY: help install dev test lint format clean run migrate

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

dev: ## Установить зависимости для разработки
	pip install -r requirements.txt
	pip install -e .

test: ## Запустить тесты
	pytest

test-cov: ## Запустить тесты с покрытием
	pytest --cov=app --cov-report=html --cov-report=term

lint: ## Проверить код линтерами
	flake8 app tests
	isort --check-only app tests

format: ## Форматировать код
	black app tests
	isort app tests

clean: ## Очистить временные файлы
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/

run: ## Запустить приложение
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate: ## Применить миграции
	alembic upgrade head

migrate-create: ## Создать новую миграцию
	@read -p "Введите описание миграции: " desc; \
	alembic revision --autogenerate -m "$$desc"

db-reset: ## Сбросить базу данных
	rm -f ecommerce.db
	alembic upgrade head

docs: ## Открыть документацию API
	@echo "Документация доступна по адресу: http://localhost:8000/docs"
	@echo "ReDoc доступен по адресу: http://localhost:8000/redoc"

check: lint test ## Проверить код и запустить тесты

all: clean install format lint test ## Полная проверка проекта
