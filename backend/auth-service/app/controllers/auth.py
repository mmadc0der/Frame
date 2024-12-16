from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt,
    verify_jwt_in_request
)
from app.models.user import User
from app.services.auth_service import AuthService
from app import db, logger

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Регистрация пользователя"""
    data = request.get_json()
    
    # Валидация входных данных
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        logger.warning("Registration attempt with invalid data", 
                      metadata={"received_fields": list(data.keys()) if data else None})
        return jsonify({"error": "Username, email and password are required"}), 400
    
    # Проверка существования пользователя
    if User.query.filter_by(email=data['email']).first():
        logger.info("Registration attempt with existing email",
                   metadata={"email": data['email']})
        return jsonify({"error": "User with this email already exists"}), 409
    if User.query.filter_by(username=data['username']).first():
        logger.info("Registration attempt with existing username",
                   metadata={"username": data['username']})
        return jsonify({"error": "User with this username already exists"}), 409
    
    # Создание нового пользователя
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    logger.info("New user registered", 
                user_id=new_user.id,
                action="user_registered",
                metadata={"username": new_user.username, "email": new_user.email})
    
    return jsonify({"message": "User successfully registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        logger.warning("Login attempt with invalid data",
                      metadata={"received_fields": list(data.keys()) if data else None})
        return jsonify({"error": "Username and password are required"}), 400

    user = AuthService.authenticate_user(data['username'], data['password'])
    if not user:
        logger.warning("Failed login attempt",
                      metadata={"username": data.get('username')})
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Генерация токенов
    access_token, refresh_token = AuthService.create_tokens(user)
    
    logger.info("User logged in",
                user_id=user.id,
                action="user_login",
                metadata={"username": user.username})
    
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
        logger.warning("Token refresh attempt without refresh token")
        return jsonify({"error": "Refresh token is required"}), 400

    user = AuthService.validate_refresh_token(refresh_token)
    if not user:
        logger.warning("Token refresh attempt with invalid token")
        return jsonify({"error": "Invalid refresh token"}), 401

    # Отзываем старый refresh токен и создаем новые токены
    AuthService.revoke_token(refresh_token)
    access_token, new_refresh_token = AuthService.create_tokens(user)

    logger.info("Tokens refreshed",
                user_id=user.id,
                action="token_refresh")

    return jsonify({
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Выход из системы"""
    user_id = get_jwt_identity()
    refresh_token = request.json.get('refresh_token')
    if refresh_token:
        AuthService.revoke_token(refresh_token)
    
    logger.info("User logged out",
                user_id=user_id,
                action="user_logout")
    
    return jsonify({"message": "Successfully logged out"}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Получение информации о текущем пользователе"""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        logger.error("User not found for token",
                    user_id=user_id,
                    action="get_user_info")
        return jsonify({"error": "User not found"}), 404
    
    logger.debug("User info requested",
                user_id=user_id,
                action="get_user_info")
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/validate', methods=['POST'])
def validate_token():
    """Валидация токена для других сервисов"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_id = get_jwt_identity()
        
        logger.debug("Token validated",
                    user_id=user_id,
                    action="validate_token",
                    metadata={"roles": claims.get('roles', [])})
        
        return jsonify({
            "valid": True,
            "user_id": user_id,
            "roles": claims.get('roles', [])
        }), 200
    except:
        logger.warning("Invalid token validation attempt",
                      action="validate_token")
        return jsonify({"valid": False}), 401
