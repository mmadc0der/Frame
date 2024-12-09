from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.models.session import SessionManager
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.get_json()
    
    # Валидация входных данных
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email и пароль обязательны"}), 400
    
    # Проверка существования пользователя
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Пользователь с таким email уже существует"}), 409
    
    # Создание нового пользователя
    new_user = User(
        username=data.get('username', data['email'].split('@')[0]),
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Неверный email или пароль"}), 401
    
    # Генерация токенов
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Сохранение сессии
    SessionManager.create_session(user.id, access_token, refresh_token)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Обновление access токена"""
    current_user_id = get_jwt_identity()
    
    # Проверка существования пользователя
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    
    # Генерация нового access токена
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({"access_token": new_access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Выход из системы"""
    current_user_id = get_jwt_identity()
    
    # Инвалидация сессии
    SessionManager.invalidate_session(current_user_id)
    
    return jsonify({"message": "Выход выполнен успешно"}), 200
