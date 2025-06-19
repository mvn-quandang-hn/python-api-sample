from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.item import ItemCreate, ItemUpdate, ItemResponse
from ..api import item as crud_item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item"""
    db_item = crud_item.create_item(db=db, item=item)
    return db_item

@router.get("/", response_model=List[ItemResponse])
async def read_items(
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = Query(None, description="Search by name"),
    db: Session = Depends(get_db)
):
    """Get all items with pagination and optional name search"""
    if name:
        items = crud_item.get_items_by_name(db, name=name, skip=skip, limit=limit)
    else:
        items = crud_item.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/low-stock", response_model=List[ItemResponse])
async def read_low_stock_items(
    threshold: int = Query(10, description="Stock threshold"),
    db: Session = Depends(get_db)
):
    """Get items with low stock"""
    items = crud_item.get_low_stock_items(db, threshold=threshold)
    return items

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """Get item by ID"""
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    """Update item"""
    db_item = crud_item.update_item(db=db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete item"""
    success = crud_item.delete_item(db=db, item_id=item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )