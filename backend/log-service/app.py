from datetime import datetime
import json
import grpc
from concurrent import futures
import log_service_pb2_grpc
from log_service_pb2 import LogResponse, LogLevel

class LogService(log_service_pb2_grpc.LogServiceBaseServicer):
    def SendLog(self, request, context):  
        try:
            level_name = LogLevel.Name(request.level)
            
            log_data = {
                'timestamp': datetime.fromtimestamp(request.timestamp).isoformat(),
                'service_name': request.service_name,
                'level': level_name,
                'message': request.message,
                'metadata': json.loads(request.metadata) if request.metadata else {},
                'user_id': request.user_id if request.HasField('user_id') else None,
                'action': request.action if request.HasField('action') else None
            }
            print(json.dumps(log_data))
            return LogResponse(success=True)
        except Exception as e:
            print(f"Error processing log: {str(e)}")
            return LogResponse(success=False, error=str(e))

def serve(host='0.0.0.0', port=5100):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_service_pb2_grpc.add_LogServiceBaseServicer_to_server(LogService(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f'Serving on {host}:{port}')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()