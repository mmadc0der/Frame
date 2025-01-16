"""Generate Python code from proto files"""
import os
import sys
from grpc_tools import protoc
import re

def fix_imports(file_path: str) -> None:
    """Fix imports in generated files"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Заменяем импорт на правильный путь
    content = content.replace(
        'import log_service_pb2 as log__service__pb2',
        'from . import log_service_pb2 as log__service__pb2'
    )
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_proto():
    """Generate Python code from proto files"""
    # Путь к директории с proto файлами
    proto_dir = os.path.abspath("../log-service/proto")
    # Путь к директории для сгенерированных файлов
    output_dir = os.path.abspath("app/proto")
    
    # Создаем директорию для сгенерированных файлов, если её нет
    os.makedirs(output_dir, exist_ok=True)
    
    # Создаем __init__.py в директории proto
    with open(os.path.join(output_dir, "__init__.py"), "w") as f:
        pass
    
    # Генерируем Python код из proto файла
    proto_file = os.path.join(proto_dir, "log_service.proto")
    
    # Используем protoc напрямую
    protoc.main([
        'grpc_tools.protoc',
        f'--proto_path={proto_dir}',
        f'--python_out={output_dir}',
        f'--grpc_python_out={output_dir}',
        proto_file
    ])
    
    # Исправляем импорты в сгенерированных файлах
    grpc_file = os.path.join(output_dir, "log_service_pb2_grpc.py")
    if os.path.exists(grpc_file):
        fix_imports(grpc_file)

if __name__ == "__main__":
    generate_proto()
