import os
from datetime import timedelta
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'postgresql://user:password@localhost/auth_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis Configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    
    # OAuth Configurations
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    YANDEX_CLIENT_ID = os.getenv('YANDEX_CLIENT_ID')
    YANDEX_CLIENT_SECRET = os.getenv('YANDEX_CLIENT_SECRET')

    # Logging Service Configuration
    LOG_SERVICE_HOST = os.getenv('LOG_SERVICE_HOST', 'localhost')
    LOG_SERVICE_PORT = int(os.getenv('LOG_SERVICE_PORT', 50051))

    # CORS Configuration
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:3000,http://localhost:8080'
    ).split(',')
    
    # Public endpoints that don't require strict CORS
    CORS_PUBLIC_ENDPOINTS = [
        '/auth/health',
        '/auth/login',
        '/auth/register',
        '/auth/oauth/github',
        '/auth/oauth/yandex'
    ]

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    # В режиме разработки разрешаем все origins
    CORS_ALLOWED_ORIGINS = ['*']

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    # В продакшене используем только безопасные настройки
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Strict'

class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CORS_ALLOWED_ORIGINS = ['*']
