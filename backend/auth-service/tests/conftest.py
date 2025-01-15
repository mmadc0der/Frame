import pytest
from unittest.mock import MagicMock, patch
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
    
    return app


@pytest.fixture(autouse=True)
def mock_redis():
    """Мок для Redis, который будет использоваться автоматически во всех тестах"""
    with patch('app.redis_client') as mock:
        mock.setex.return_value = True
        mock.get.return_value = None
        mock.delete.return_value = True
        yield mock


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


@pytest.fixture
def access_token(client, db_session):
    """Фикстура для получения тестового access токена"""
    # Регистрируем тестового пользователя
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Логинимся и получаем токен
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    return response.json['access_token']
