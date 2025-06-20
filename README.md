## **🔄 Cấu trúc thư mục (Modular Architecture):**

```
# Cấu trúc thư mục mới:
# project/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── database.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   └── item.py
# │   ├── schemas/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   └── item.py
# │   ├── api/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   └── item.py
# │   └── routers/
# │       ├── __init__.py
# │       ├── users.py
# │       └── items.py
# ├── tests/
# │   ├── __init__.py
# │   ├── test_users.py
# │   └── test_items.py
# ├── requirements.txt
# ├── Dockerfile
# └── docker-compose.yml
```

## **🧪 Unit Tests hoàn chỉnh:**

### **Test coverage:**

- `tests/test_users.py` - 8 test cases cho users
- `tests/test_items.py` - 15+ test cases cho items
- Bao gồm: CRUD, validation, search, pagination, error cases

## **🚀 Cách sử dụng:**

bash

```bash
# 1. Start services
docker-compose up --build

# 2. API endpoints
# Users: http://localhost:8000/users/
# Items: http://localhost:8000/items/
# Docs: http://localhost:8000/docs

# 3. Chạy tests
pytest tests/ -v                # Tất cả tests
pytest tests/test_users.py -v   # Chỉ user tests  
pytest tests/test_items.py -v   # Chỉ item tests
```

## **📝 Ví dụ sử dụng:**

json

```json
// Tạo item mới
POST /items/
{
  "name": "iPhone 15",
  "memo": "Latest model",
  "quantity": 50,
  "price": "999.99"
}

// Search items
GET /items/?name=iPhone

// Low stock items
GET /items/low-stock?threshold=10
```
