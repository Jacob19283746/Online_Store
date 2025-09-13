#!/usr/bin/env python3
"""
Скрипт для быстрого запуска приложения
"""
import uvicorn
import os
import sys

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Запуск Online Store API...")
    print("📚 Документация: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("🔧 API: http://localhost:8000/api/v1/")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )
