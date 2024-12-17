import pytest
from app.models.user import User
from app.models.role import Role, Permission

def test_register(client, db_session):
    """Тест регистрации пользователя"""
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 201
    assert b'successfully registered' in response.data

    # Проверяем, что пользователь создан в БД
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'test@example.com'

def test_register_duplicate_email(client, db_session):
    """Тест регистрации с существующим email"""
    # Создаем первого пользователя
    client.post('/auth/register', json={
        'username': 'user1',
        'email': 'test@example.com',
        'password': 'pass123'
    })

    # Пытаемся создать второго с тем же email
    response = client.post('/auth/register', json={
        'username': 'user2',
        'email': 'test@example.com',
        'password': 'pass123'
    })
    assert response.status_code == 409

def test_login_success(client, db_session):
    """Тест успешного входа"""
    # Регистрируем пользователя
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })

    # Пробуем войти
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_login_invalid_credentials(client, db_session):
    """Тест входа с неверными данными"""
    response = client.post('/auth/login', json={
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    assert response.status_code == 401

@pytest.fixture
def access_token(client, db_session):
    """Фикстура для получения токена"""
    # Регистрируем пользователя
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })

    # Входим и получаем токен
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    return response.json['access_token']

def test_me_endpoint(client, db_session, access_token):
    """Тест получения информации о пользователе"""
    response = client.get('/auth/me', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'test@example.com'

def test_me_no_token(client):
    """Тест доступа к /me без токена"""
    response = client.get('/auth/me')
    assert response.status_code == 401

def test_validate_token(client, access_token):
    """Тест валидации токена"""
    response = client.post('/auth/validate', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    assert response.json['valid'] is True

def test_validate_invalid_token(client):
    """Тест валидации неверного токена"""
    response = client.post('/auth/validate', headers={
        'Authorization': 'Bearer invalid_token'
    })
    assert response.status_code == 422
    assert response.json['valid'] is False
