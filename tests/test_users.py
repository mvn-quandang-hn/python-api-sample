import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup database before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    """Test creating a user"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data

def test_create_user_duplicate_email():
    """Test creating user with duplicate email"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    # Create first user
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same email
    response2 = client.post("/users/", json=user_data)
    assert response2.status_code == 400
    assert "Email already exists" in response2.json()["detail"]

def test_get_users():
    """Test getting all users"""
    users_data = [
        {"name": "User 1", "email": "user1@example.com", "password": "password1"},
        {"name": "User 2", "email": "user2@example.com", "password": "password2"}
    ]
    
    for user_data in users_data:
        client.post("/users/", json=user_data)
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_user_by_id():
    """Test getting user by ID"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]

def test_get_user_not_found():
    """Test getting non-existent user"""
    response = client.get("/users/999")
    assert response.status_code == 404

def test_update_user():
    """Test updating user"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated User",
        "email": "updated@example.com"
    }
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]

def test_update_user_not_found():
    """Test updating non-existent user"""
    update_data = {"name": "Updated User"}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404

def test_delete_user():
    """Test deleting user"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_delete_user_not_found():
    """Test deleting non-existent user"""
    response = client.delete("/users/999")
    assert response.status_code == 404