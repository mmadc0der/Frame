from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt,
    verify_jwt_in_request
)
from app.models.user import User
from app.services.auth_service import AuthService
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Регистрация пользователя"""
    data = request.get_json()
    
    # Валидация входных данных
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({"error": "Username, email and password are required"}), 400
    
    # Проверка существования пользователя
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User with this email already exists"}), 409
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User with this username already exists"}), 409
    
    # Создание нового пользователя
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User successfully registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    user = AuthService.authenticate_user(data['username'], data['password'])
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Генерация токенов
    access_token, refresh_token = AuthService.create_tokens(user)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Обновление access токена"""
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({"error": "Refresh token is required"}), 400

    user = AuthService.validate_refresh_token(refresh_token)
    if not user:
        return jsonify({"error": "Invalid refresh token"}), 401

    # Отзываем старый refresh токен и создаем новые токены
    AuthService.revoke_token(refresh_token)
    access_token, new_refresh_token = AuthService.create_tokens(user)

    return jsonify({
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Выход из системы"""
    refresh_token = request.json.get('refresh_token')
    if refresh_token:
        AuthService.revoke_token(refresh_token)
    return jsonify({"message": "Successfully logged out"}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Получение информации о текущем пользователе"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@auth_bp.route('/validate', methods=['POST'])
def validate_token():
    """Валидация токена для других сервисов"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        return jsonify({
            "valid": True,
            "user_id": get_jwt_identity(),
            "roles": claims.get('roles', [])
        }), 200
    except:
        return jsonify({"valid": False}), 401
