from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis
from .services.log_service import LogService
from flask_cors import CORS

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
    
    # Инициализация CORS
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})  # Разрешить доступ с любых источников

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
