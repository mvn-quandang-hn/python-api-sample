from sqlalchemy.orm import Session
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate
from typing import List, Optional

def create_item(db: Session, item: ItemCreate) -> Item:
    """Create a new item"""
    db_item = Item(
        name=item.name,
        memo=item.memo,
        quantity=item.quantity,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Get item by ID"""
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get all items with pagination"""
    return db.query(Item).offset(skip).limit(limit).all()

def get_items_by_name(db: Session, name: str, skip: int = 0, limit: int = 100) -> List[Item]:
    """Search items by name"""
    return db.query(Item).filter(Item.name.ilike(f"%{name}%")).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    """Update item"""
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    update_data = item_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    """Delete item"""
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True

def get_low_stock_items(db: Session, threshold: int = 10) -> List[Item]:
    """Get items with low stock"""
    return db.query(Item).filter(Item.quantity <= threshold).all()