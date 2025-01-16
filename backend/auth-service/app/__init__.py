from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis
from .services.log_service import LogService

# Инициализация глобальных объектов
db = SQLAlchemy()
jwt = JWTManager()
redis_client = redis.Redis(host='localhost', port=6379, db=0)
logger = LogService()

def create_app(config_object='app.config.Config'):
    """Создание и конфигурация Flask приложения"""
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object(config_object)
    
    # Инициализация расширений
    db.init_app(app)
    jwt.init_app(app)

    # Настройка CORS с помощью встроенного механизма Flask
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        
        # Определяем, является ли текущий эндпоинт публичным
        is_public_endpoint = any(
            request.path.startswith(endpoint) 
            for endpoint in app.config['CORS_PUBLIC_ENDPOINTS']
        )

        # Для публичных эндпоинтов используем менее строгие правила
        if is_public_endpoint:
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        # Для защищенных эндпоинтов используем строгие правила
        else:
            # Проверяем, разрешен ли origin
            if origin in app.config['CORS_ALLOWED_ORIGINS'] or app.config['CORS_ALLOWED_ORIGINS'] == ['*']:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = (
                    'Content-Type, Authorization, X-Requested-With'
                )
                # Добавляем дополнительные заголовки безопасности
                if not app.config['DEBUG']:
                    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
                    response.headers['X-XSS-Protection'] = '1; mode=block'
            else:
                # Если origin не разрешен, удаляем CORS заголовки и возвращаем 403
                response.headers.pop('Access-Control-Allow-Origin', None)
                response.status_code = 403

        # Для OPTIONS запросов возвращаем пустой ответ
        if request.method == 'OPTIONS':
            return response

        return response

    # Регистрация блюпринтов
    from .controllers.auth import auth_bp
    from .controllers.oauth import oauth_bp
    from .controllers.health import health_bp
    from .controllers.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(oauth_bp, url_prefix='/auth/oauth')
    app.register_blueprint(health_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/auth/admin')
    
    return app
