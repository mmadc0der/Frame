import pytest
from unittest.mock import MagicMock
from app import create_app, db, redis_client


@pytest.fixture
def app():
    """Создание тестового приложения"""
    app = create_app('app.config.TestingConfig')
    
    # Добавляем тестовые CORS настройки
    app.config.update({
        'CORS_ALLOWED_ORIGINS': ['*'],  # В тестах разрешаем все origins
        'CORS_PUBLIC_ENDPOINTS': [
            '/auth/health',
            '/auth/login',
            '/auth/register',
            '/auth/oauth/github',
            '/auth/oauth/yandex'
        ]
    })
    
    # Мокаем Redis для тестов
    redis_mock = MagicMock()
    redis_mock.setex.return_value = True
    redis_mock.get.return_value = None
    redis_mock.delete.return_value = True
    app.redis_client = redis_mock
    
    return app


@pytest.fixture
def client(app):
    """Создание тестового клиента"""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Создание тестовой сессии БД"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
