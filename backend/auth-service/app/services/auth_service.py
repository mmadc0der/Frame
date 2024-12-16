from datetime import datetime, timezone
import json
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db, redis_client
from app.models.user import User

class AuthService:
    @staticmethod
    def create_tokens(user):
        """Создание access и refresh токенов"""
        # Добавляем роли в claims токена
        additional_claims = {'roles': user.get_roles()}
        
        # Создаем токены
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(identity=user.id)

        # Сохраняем информацию о refresh токене в Redis
        session_data = {
            'user_id': user.id,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        redis_client.setex(
            f'refresh_token:{refresh_token}',
            60 * 60 * 24 * 30,  # 30 дней
            json.dumps(session_data)
        )

        return access_token, refresh_token

    @staticmethod
    def validate_refresh_token(refresh_token):
        """Проверка refresh токена в Redis"""
        session_key = f'refresh_token:{refresh_token}'
        session_data = redis_client.get(session_key)
        if not session_data:
            return None
        
        session = json.loads(session_data)
        return db.session.get(User, session['user_id'])

    @staticmethod
    def revoke_token(refresh_token):
        """Отзыв refresh токена"""
        session_key = f'refresh_token:{refresh_token}'
        redis_client.delete(session_key)

    @staticmethod
    def authenticate_user(username, password):
        """Аутентификация пользователя по username и паролю"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            return user
        return None
