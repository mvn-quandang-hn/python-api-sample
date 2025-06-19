from fastapi import FastAPI
from .database import engine
from .models import User, Item
from .routers import users, items

# Create tables
User.metadata.create_all(bind=engine)
Item.metadata.create_all(bind=engine)

app = FastAPI(
    title="User & Item CRUD API",
    description="API for managing users and items",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "User & Item CRUD API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}