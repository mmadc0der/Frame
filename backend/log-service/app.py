from datetime import datetime
import json
from grpclib.server import Server
from grpclib.utils import graceful_exit
from proto.log_service_grpc import LogServiceBase, LogServiceStub

class LogService(LogServiceBase):
    async def send_log(self, message):
        """
        Временная заглушка для приема логов.
        В будущем будет сохранять в ClickHouse.
        """
        log_data = {
            'timestamp': datetime.fromtimestamp(message.timestamp).isoformat(),
            'service_name': message.service_name,
            'level': message.level.name,
            'message': message.message,
            'metadata': json.loads(message.metadata) if message.metadata else {},
            'user_id': message.user_id if message.HasField('user_id') else None,
            'action': message.action if message.HasField('action') else None
        }
        
        # Пока просто выводим в консоль
        print(f"[LOG] {json.dumps(log_data, indent=2)}")
        
        return {'success': True}

    async def get_logs(self, request):
        """
        Временная заглушка для получения логов.
        В будущем будет получать из ClickHouse.
        """
        return {
            'logs': [],
            'total_count': 0,
            'page_number': request.page_number,
            'page_size': request.page_size
        }

async def main(host='0.0.0.0', port=50051):
    server = Server([LogService()])
    with graceful_exit([server]):
        await server.start(host, port)
        print(f'Serving on {host}:{port}')
        await server.wait_closed()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
