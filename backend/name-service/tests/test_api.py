from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_generate_name_default(client):
    """Test name generation with default parameters"""
    response = client.post("/generate", json={})
    assert response.status_code == 200
    assert "username" in response.json()
    username = response.json()["username"]
    assert isinstance(username, str)
    assert len(username) > 0

def test_generate_name_with_prefix(client):
    """Test name generation with prefix"""
    prefix = "test"
    response = client.post("/generate", json={"prefix": prefix})
    assert response.status_code == 200
    assert "username" in response.json()
    username = response.json()["username"]
    assert username.startswith(prefix)

def test_generate_name_with_styles(client):
    """Test name generation with different styles"""
    styles = ["default", "funny", "serious"]
    for style in styles:
        response = client.post("/generate", json={"style": style})
        assert response.status_code == 200
        assert "username" in response.json()

def test_generate_name_invalid_style(client):
    """Test name generation with invalid style"""
    response = client.post("/generate", json={"style": "invalid_style"})
    assert response.status_code == 400
    assert "detail" in response.json()

def test_generate_name_with_prefix_and_style(client):
    """Test name generation with both prefix and style"""
    response = client.post("/generate", json={
        "prefix": "test",
        "style": "funny"
    })
    assert response.status_code == 200
    assert "username" in response.json()
    username = response.json()["username"]
    assert username.startswith("test")
