import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from decimal import Decimal

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_items.db"
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

def test_create_item():
    """Test creating an item"""
    item_data = {
        "name": "Test Item",
        "memo": "This is a test item",
        "quantity": 10,
        "price": "19.99"
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["memo"] == item_data["memo"]
    assert data["quantity"] == item_data["quantity"]
    assert float(data["price"]) == float(item_data["price"])
    assert "id" in data

def test_create_item_minimal():
    """Test creating item with minimal data"""
    item_data = {
        "name": "Minimal Item",
        "quantity": 5,
        "price": "9.99"
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["memo"] is None
    assert data["quantity"] == item_data["quantity"]

def test_create_item_invalid_quantity():
    """Test creating item with negative quantity"""
    item_data = {
        "name": "Invalid Item",
        "quantity": -1,
        "price": "10.00"
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 422

def test_create_item_invalid_price():
    """Test creating item with negative price"""
    item_data = {
        "name": "Invalid Item",
        "quantity": 10,
        "price": "-5.00"
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 422

def test_get_items():
    """Test getting all items"""
    items_data = [
        {"name": "Item 1", "quantity": 10, "price": "10.00"},
        {"name": "Item 2", "quantity": 20, "price": "20.00"}
    ]
    
    for item_data in items_data:
        client.post("/items/", json=item_data)
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_item_by_id():
    """Test getting item by ID"""
    item_data = {
        "name": "Test Item",
        "memo": "Test memo",
        "quantity": 15,
        "price": "25.99"
    }
    
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == item_data["name"]

def test_get_item_not_found():
    """Test getting non-existent item"""
    response = client.get("/items/999")
    assert response.status_code == 404

def test_search_items_by_name():
    """Test searching items by name"""
    items_data = [
        {"name": "Apple Phone", "quantity": 10, "price": "999.00"},
        {"name": "Apple Watch", "quantity": 5, "price": "399.00"},
        {"name": "Samsung Phone", "quantity": 8, "price": "799.00"}
    ]
    
    for item_data in items_data:
        client.post("/items/", json=item_data)
    
    response = client.get("/items/?name=Apple")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("Apple" in item["name"] for item in data)

def test_get_low_stock_items():
    """Test getting low stock items"""
    items_data = [
        {"name": "Low Stock Item 1", "quantity": 5, "price": "10.00"},
        {"name": "Low Stock Item 2", "quantity": 8, "price": "15.00"},
        {"name": "High Stock Item", "quantity": 50, "price": "20.00"}
    ]
    
    for item_data in items_data:
        client.post("/items/", json=item_data)
    
    response = client.get("/items/low-stock?threshold=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["quantity"] <= 10 for item in data)

def test_update_item():
    """Test updating item"""
    item_data = {
        "name": "Original Item",
        "memo": "Original memo",
        "quantity": 10,
        "price": "19.99"
    }
    
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated Item",
        "quantity": 20,
        "price": "29.99"
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["quantity"] == update_data["quantity"]
    assert float(data["price"]) == float(update_data["price"])
    assert data["memo"] == item_data["memo"]  # Should remain unchanged

def test_update_item_partial():
    """Test partial update of item"""
    item_data = {
        "name": "Test Item",
        "quantity": 10,
        "price": "19.99"
    }
    
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    update_data = {"quantity": 15}
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 15
    assert data["name"] == item_data["name"]  # Should remain unchanged

def test_update_item_not_found():
    """Test updating non-existent item"""
    update_data = {"name": "Updated Item"}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404

def test_delete_item():
    """Test deleting item"""
    item_data = {
        "name": "Test Item",
        "quantity": 10,
        "price": "19.99"
    }
    
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_delete_item_not_found():
    """Test deleting non-existent item"""
    response = client.delete("/items/999")
    assert response.status_code == 404

def test_pagination_items():
    """Test pagination for items"""
    # Create 5 items
    for i in range(5):
        item_data = {
            "name": f"Item {i}",
            "quantity": i + 1,
            "price": f"{(i + 1) * 10}.00"
        }
        client.post("/items/", json=item_data)
    
    # Test pagination
    response = client.get("/items/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 2"
    assert data[1]["name"] == "Item 3"

def test_item_validation():
    """Test item field validation"""
    # Test empty name
    response = client.post("/items/", json={
        "name": "",
        "quantity": 10,
        "price": "19.99"
    })
    assert response.status_code == 422
    
    # Test missing required fields
    response = client.post("/items/", json={
        "name": "Test Item"
    })
    assert response.status_code == 422