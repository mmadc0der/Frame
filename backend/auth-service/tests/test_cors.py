def test_public_endpoint_cors(client):
    """Тест CORS для публичного эндпоинта"""
    # Проверяем OPTIONS запрос к публичному эндпоинту
    response = client.options('/auth/login', headers={
        'Origin': 'http://example.com',
        'Access-Control-Request-Method': 'POST'
    })
    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == '*'
    assert 'POST' in response.headers['Access-Control-Allow-Methods']
    assert 'Content-Type' in response.headers['Access-Control-Allow-Headers']

    # Проверяем обычный запрос
    response = client.get('/auth/health', headers={
        'Origin': 'http://example.com'
    })
    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == '*'


def test_protected_endpoint_cors(client, access_token):
    """Тест CORS для защищенного эндпоинта"""
    # Проверяем OPTIONS запрос к защищенному эндпоинту
    response = client.options('/auth/me', headers={
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Authorization'
    })
    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
    assert 'GET' in response.headers['Access-Control-Allow-Methods']
    assert 'Authorization' in response.headers['Access-Control-Allow-Headers']
    assert response.headers['Access-Control-Allow-Credentials'] == 'true'

    # Проверяем обычный запрос с валидным origin
    response = client.get('/auth/me', 
        headers={
            'Origin': 'http://localhost:3000',
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
    assert response.headers['Access-Control-Allow-Credentials'] == 'true'


def test_protected_endpoint_invalid_origin(client, access_token):
    """Тест CORS с неразрешенным origin для защищенного эндпоинта"""
    # В тестовом окружении все origins разрешены, поэтому временно меняем настройку
    from flask import current_app
    current_app.config['CORS_ALLOWED_ORIGINS'] = ['http://localhost:3000']

    response = client.get('/auth/me', 
        headers={
            'Origin': 'http://evil.com',
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 403
    assert 'Access-Control-Allow-Origin' not in response.headers
