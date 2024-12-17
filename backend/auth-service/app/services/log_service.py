import json
import time
from enum import Enum
from typing import Optional, Dict, Any

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class LogService:
    """
    Клиент для отправки логов в сервис логирования.
    Пока что это заглушка, которая будет заменена на реальный GRPC клиент.
    """
    def __init__(self, service_name: str = "auth-service"):
        self.service_name = service_name
        # TODO: Инициализация GRPC клиента
        # self.stub = ...

    def _prepare_metadata(self, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Подготовка метаданных для отправки"""
        return json.dumps(metadata or {})

    def send_log(
        self,
        message: str,
        level: LogLevel,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Отправка лога в сервис логирования
        
        Args:
            message: Сообщение лога
            level: Уровень логирования
            user_id: ID пользователя (если применимо)
            action: Действие пользователя (если применимо)
            metadata: Дополнительные метаданные
        """
        log_data = {
            "timestamp": int(time.time()),
            "service_name": self.service_name,
            "level": level.value,
            "message": message,
            "metadata": self._prepare_metadata(metadata),
        }
        
        if user_id is not None:
            log_data["user_id"] = user_id
        if action is not None:
            log_data["action"] = action

        # TODO: Отправка через GRPC
        # response = self.stub.SendLog(log_message)
        # Пока просто выводим в консоль
        print(f"[LOG] {json.dumps(log_data)}")

    def debug(self, message: str, **kwargs):
        self.send_log(message, LogLevel.DEBUG, **kwargs)

    def info(self, message: str, **kwargs):
        self.send_log(message, LogLevel.INFO, **kwargs)

    def warning(self, message: str, **kwargs):
        self.send_log(message, LogLevel.WARNING, **kwargs)

    def error(self, message: str, **kwargs):
        self.send_log(message, LogLevel.ERROR, **kwargs)

    def critical(self, message: str, **kwargs):
        self.send_log(message, LogLevel.CRITICAL, **kwargs)
