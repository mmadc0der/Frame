import json
import time
from enum import Enum
from typing import Optional, Dict, Any
import grpc
from app.proto import log_service_pb2
from app.proto import log_service_pb2_grpc
from flask import current_app

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class LogService:
    """Клиент для отправки логов в сервис логирования через GRPC."""
    
    def __init__(self, service_name: str = "auth-service"):
        self.service_name = service_name
        self._stub = None

    @property
    def stub(self):
        """Ленивая инициализация GRPC stub"""
        if self._stub is None:
            # Создаем канал для связи с сервисом логирования
            channel = grpc.insecure_channel(
                f"{current_app.config['LOG_SERVICE_HOST']}:{current_app.config['LOG_SERVICE_PORT']}"
            )
            self._stub = log_service_pb2_grpc.LogServiceBaseStub(channel)
        return self._stub

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
        try:
            # Создаем сообщение для отправки
            log_message = log_service_pb2.LogMessage(
                timestamp=int(time.time()),
                service_name=self.service_name,
                level=level.value,
                message=message,
                metadata=self._prepare_metadata(metadata),
                user_id=user_id,
                action=action
            )
            
            # Отправляем лог
            response = self.stub.SendLog(log_message)
            
            if not response.success:
                print(f"Failed to send log: {response.error}")
                
        except grpc.RpcError as e:
            print(f"GRPC Error while sending log: {str(e)}")
        except Exception as e:
            print(f"Unexpected error while sending log: {str(e)}")

    def debug(self, message: str, user_id: Optional[int] = None, action: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.send_log(message, LogLevel.DEBUG, user_id, action, metadata)

    def info(self, message: str, user_id: Optional[int] = None, action: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.send_log(message, LogLevel.INFO, user_id, action, metadata)

    def warning(self, message: str, user_id: Optional[int] = None, action: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.send_log(message, LogLevel.WARNING, user_id, action, metadata)

    def error(self, message: str, user_id: Optional[int] = None, action: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.send_log(message, LogLevel.ERROR, user_id, action, metadata)

    def critical(self, message: str, user_id: Optional[int] = None, action: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.send_log(message, LogLevel.CRITICAL, user_id, action, metadata)
