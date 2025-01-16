import requests
from typing import Optional
from flask import current_app
import logging

class NameService:
    """Клиент для взаимодействия с сервисом генерации имен"""
    
    def __init__(self):
        self.base_url = f"http://{current_app.config['NAME_SERVICE_HOST']}:{current_app.config['NAME_SERVICE_PORT']}"
        
    def generate_username(self, prefix: Optional[str] = None, style: str = "default") -> str:
        """
        Генерация уникального имени пользователя
        
        Args:
            prefix: Префикс для имени пользователя (опционально)
            style: Стиль генерации имени (default, funny, serious)
            
        Returns:
            str: Сгенерированное имя пользователя
            
        Raises:
            RuntimeError: Если сервис недоступен или вернул ошибку
        """
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json={"prefix": prefix, "style": style},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()["username"]
            else:
                error_msg = f"Name service error: {response.status_code} - {response.text}"
                logging.error(error_msg)
                raise RuntimeError(error_msg)
                
        except requests.RequestException as e:
            error_msg = f"Failed to connect to name service: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)
