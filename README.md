1. Cấp trúc app:
app/
├── models/         # Database models
│   ├── user.py
│   └── item.py
├── schemas/        # Pydantic schemas  
│   ├── user.py
│   └── item.py
├── api/          # Database operations
│   ├── user.py
│   └── item.py
└── routers/       # API endpoints
    ├── users.py
    └── items.py

🚀 **Cách sử dụng:**
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

📝 **Ví dụ sử dụng:**
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
