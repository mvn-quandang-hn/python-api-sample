from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ItemBase(BaseModel):
    name: str
    memo: Optional[str] = None
    quantity: int = Field(ge=0, description="Quantity must be >= 0")
    price: Decimal = Field(ge=0, description="Price must be >= 0")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    memo: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0, description="Quantity must be >= 0")
    price: Optional[Decimal] = Field(None, ge=0, description="Price must be >= 0")

class ItemResponse(ItemBase):
    id: int
    
    class Config:
        from_attributes = True