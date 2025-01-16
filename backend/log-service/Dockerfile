# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Компилируем proto файлы
RUN python -m grpc_tools.protoc \
    -I proto \
    --python_out=. \
    --grpc_python_out=. \
    proto/log_service.proto

# Открываем порт для gRPC
EXPOSE 5100

# Команда для запуска приложения
CMD ["python", "app.py"]
