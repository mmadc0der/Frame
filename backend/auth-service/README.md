# Frame Auth Service

Сервис аутентификации для проекта Frame.

## Функциональность

- Регистрация и аутентификация пользователей
- Управление сессиями через Redis
- JWT токены для авторизации
- Управление ролями и правами
- Валидация токенов для других сервисов
- GRPC интеграция с сервисом логирования

## API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Вход в систему
- `POST /auth/refresh` - Обновление access токена
- `POST /auth/logout` - Выход из системы
- `GET /auth/me` - Информация о текущем пользователе
- `POST /auth/validate` - Валидация токена (для других сервисов)

### Администрирование
- `GET /auth/admin/roles` - Получение списка ролей
- `POST /auth/admin/roles` - Создание новой роли
- `GET /auth/admin/permissions` - Получение списка прав
- `POST /auth/admin/permissions` - Создание нового права
- `PUT /auth/admin/roles/{role_id}/permissions` - Обновление прав роли
- `PUT /auth/admin/users/{user_id}/roles` - Обновление ролей пользователя

## Настройка окружения

1. Установка зависимостей:
```bash
pip install -r requirements.txt
```

2. Настройка переменных окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл
```

3. Запуск PostgreSQL:
```bash
docker-compose up -d postgres
```

4. Запуск Redis:
```bash
docker-compose up -d redis
```

## Запуск тестов

```bash
pytest tests/
```

## Структура проекта

```
auth-service/
├── app/
│   ├── controllers/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── health.py
│   │   └── oauth.py
│   ├── models/
│   │   ├── role.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── log_service.py
│   └── __init__.py
├── tests/
│   ├── test_admin.py
│   ├── test_auth.py
│   └── conftest.py
├── config.py
└── run.py
```

## Логирование

Сервис использует GRPC для отправки логов в центральный сервис логирования. События логируются с различными уровнями:

- DEBUG - Отладочная информация
- INFO - Успешные операции
- WARNING - Подозрительные действия
- ERROR - Ошибки выполнения

## База данных

### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    full_name VARCHAR(255),
    phone_number VARCHAR(15),
    gender VARCHAR(10),
    birth_date DATE,
    provider VARCHAR(50),
    provider_user_id VARCHAR(255),
    provider_data JSONB
);
```

### Roles & Permissions
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id),
    permission_id INT REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
    user_id INT REFERENCES users(id),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```
