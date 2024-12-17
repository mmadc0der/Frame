import pytest
from app.models.role import Role, Permission
from app.models.user import User

@pytest.fixture
def admin_token(client, db_session):
    """Фикстура для создания админа и получения его токена"""
    # Создаем роль админа
    admin_role = Role(name='admin')
    db_session.add(admin_role)
    
    # Регистрируем админа
    client.post('/auth/register', json={
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    
    # Назначаем роль админа
    user = User.query.filter_by(username='admin').first()
    user.roles.append(admin_role)
    db_session.commit()
    
    # Получаем токен
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'adminpass123'
    })
    return response.json['access_token']

def test_create_role(client, db_session, admin_token):
    """Тест создания роли"""
    response = client.post('/auth/admin/roles', 
        json={'name': 'test_role', 'description': 'Test role'},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 201
    assert response.json['name'] == 'test_role'
    
    # Проверяем, что роль создана в БД
    role = Role.query.filter_by(name='test_role').first()
    assert role is not None
    assert role.description == 'Test role'

def test_create_role_unauthorized(client, db_session):
    """Тест создания роли без прав админа"""
    # Создаем обычного пользователя и получаем его токен
    client.post('/auth/register', json={
        'username': 'user',
        'email': 'user@example.com',
        'password': 'userpass123'
    })
    response = client.post('/auth/login', json={
        'username': 'user',
        'password': 'userpass123'
    })
    token = response.json['access_token']
    
    # Пытаемся создать роль
    response = client.post('/auth/admin/roles',
        json={'name': 'test_role'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403

def test_create_permission(client, db_session, admin_token):
    """Тест создания права"""
    response = client.post('/auth/admin/permissions',
        json={'name': 'test_permission', 'description': 'Test permission'},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 201
    assert response.json['name'] == 'test_permission'

def test_update_role_permissions(client, db_session, admin_token):
    """Тест обновления прав роли"""
    # Создаем роль и право
    role_response = client.post('/auth/admin/roles',
        json={'name': 'test_role'},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    perm_response = client.post('/auth/admin/permissions',
        json={'name': 'test_permission'},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    role_id = role_response.json['id']
    
    # Обновляем права роли
    response = client.put(f'/auth/admin/roles/{role_id}/permissions',
        json={'permissions': ['test_permission']},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    assert 'test_permission' in response.json['permissions']

def test_update_user_roles(client, db_session, admin_token):
    """Тест обновления ролей пользователя"""
    # Создаем роль и пользователя
    client.post('/auth/admin/roles',
        json={'name': 'test_role'},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    user = User.query.filter_by(username='testuser').first()
    
    # Назначаем роль пользователю
    response = client.put(f'/auth/admin/users/{user.id}/roles',
        json={'roles': ['test_role']},
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    assert 'test_role' in response.json['roles']
