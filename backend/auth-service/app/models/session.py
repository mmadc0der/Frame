import json
from app import redis_client
from datetime import timedelta

class SessionManager:
    """Менеджер сессий с использованием Redis"""
    
    @staticmethod
    def create_session(user_id, access_token, refresh_token):
        """Создание новой сессии"""
        session_data = {
            'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        
        # Храним сессию в Redis с TTL
        redis_client.setex(
            f'session:{user_id}', 
            timedelta(days=30),  # Срок жизни сессии
            json.dumps(session_data)
        )
    
    @staticmethod
    def get_session(user_id):
        """Получение данных сессии"""
        session_json = redis_client.get(f'session:{user_id}')
        return json.loads(session_json) if session_json else None
    
    @staticmethod
    def invalidate_session(user_id):
        """Инвалидация сессии"""
        redis_client.delete(f'session:{user_id}')
    
    @staticmethod
    def is_token_blacklisted(token):
        """Проверка токена в черном списке"""
        return redis_client.sismember('blacklisted_tokens', token)
    
    @staticmethod
    def blacklist_token(token):
        """Добавление токена в черный список"""
        redis_client.sadd('blacklisted_tokens', token)
