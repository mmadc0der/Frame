# Frame - Personal Daily Journal

![Auth Service CI](https://github.com/mmadc0der/Frame/tree/main/backend/auth-service)

Микросервисное приложение для создания персонализированного ежедневника с модульной структурой.

## Архитектура

Проект состоит из следующих компонентов:

### Frontend
- Визитка (Landing page)
- Основной функционал (после аутентификации)
- Админ-панель

### Backend
- **Auth Service** - Сервис аутентификации
  - PostgreSQL для данных пользователей
  - Redis для сессий
  - JWT токены для авторизации
- **Central Service** - Центральный сервис
  - Основная бизнес-логика
  - PostgreSQL для данных
- **Log Service** - Сервис логирования
  - ClickHouse для хранения логов
  - GRPC API для приема логов

## Коммуникация между сервисами
- GRPC для логирования
- REST API для остальных взаимодействий

## Модули ежедневника
1. Приветствие и дата (всегда включен)
2. Погода
3. Цитата/Анекдот/Факт дня
4. Список дел
5. Заметки

## Разработка

### Требования
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- ClickHouse

### Настройка окружения

1. Клонирование репозитория:
```bash
git clone https://github.com/yourusername/Frame.git
cd Frame
```

2. Настройка сервиса аутентификации:
```bash
cd backend/auth-service
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

3. Настройка переменных окружения:
- Скопируйте `.env.example` в `.env` в каждом сервисе
- Заполните необходимые переменные окружения

### Запуск тестов

```bash
# Auth Service
cd backend/auth-service
pytest tests/
```

### Запуск сервисов

1. Auth Service:
```bash
cd backend/auth-service
python run.py
```

2. Log Service (в разработке):
```bash
cd backend/log-service
python run.py
```

## Лицензия

MIT
