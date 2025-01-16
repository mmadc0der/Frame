import grpc
import time
from log_service_pb2_grpc import LogServiceBaseStub
from log_service_pb2 import LogMessage, LogLevel

def run():
    with grpc.insecure_channel('localhost:5100') as channel:
        stub = LogServiceBaseStub(channel)
        
        # Создаем тестовое сообщение
        message = LogMessage(
            timestamp=int(time.time()),
            service_name="test_service",
            level=LogLevel.INFO,
            message="Test log message",
            metadata='{"test": "metadata"}',
            user_id=123,
            action="test_action"
        )
        
        # Отправляем сообщение
        response = stub.SendLog(message)
        print(f"Response received: {response.success}")

if __name__ == '__main__':
    run()