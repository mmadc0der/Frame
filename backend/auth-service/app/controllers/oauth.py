from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
import requests
from app.models.user import User
from app import db, config

oauth_bp = Blueprint('oauth', __name__)

def get_github_access_token(code):
    """Получение access токена от GitHub"""
    params = {
        'client_id': config.Config.GITHUB_CLIENT_ID,
        'client_secret': config.Config.GITHUB_CLIENT_SECRET,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', params=params, headers=headers)
    return response.json().get('access_token')

def get_github_user_info(access_token):
    """Получение информации о пользователе от GitHub"""
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    return response.json()

@oauth_bp.route('/github/callback', methods=['POST'])
def github_callback():
    """Обработка OAuth колбэка от GitHub"""
    code = request.json.get('code')
    
    # Получение токена доступа
    github_access_token = get_github_access_token(code)
    
    # Получение информации о пользователе
    github_user = get_github_user_info(github_access_token)
    
    # Поиск или создание пользователя
    user = db.session.query(User).filter_by(email=github_user['email']).first()
    
    if not user:
        user = User(
            username=github_user['login'],
            email=github_user['email']
        )
        db.session.add(user)
        db.session.commit()
    
    # Генерация токенов
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200
