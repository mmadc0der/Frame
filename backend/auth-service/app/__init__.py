from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis

# Инициализация глобальных объектов
db = SQLAlchemy()
jwt = JWTManager()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def create_app(config_object='app.config.Config'):
    """Создание и конфигурация Flask приложения"""
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object(config_object)
    
    # Инициализация расширений
    db.init_app(app)
    jwt.init_app(app)
    
    # Регистрация блюпринтов
    from .controllers.auth import auth_bp
    from .controllers.oauth import oauth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(oauth_bp, url_prefix='/auth/oauth')
    
    return app
