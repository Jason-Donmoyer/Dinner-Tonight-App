from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.recipe import InventoryItem
from app.models.recipe import UserInventory, Ingredient

router = APIRouter()

@router.get("/", response_model=List[InventoryItem])
def get_inventory(
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get user's current inventory
    """
    items = db.query(UserInventory).filter(
        UserInventory.user_id == user_id
    ).all()

    return [
        InventoryItem(
            id=item.id,
            ingredient=item.ingredient,
            ingredient_id=item.ingredient_id,
            quantity=float(item.quantity) if item.quantity else None,
            unit=item.unit
        )
        for item in items
    ]

@router.post("/", status_code=201)
def add_to_inverntory(
    ingredient_id: int = Query(..., description="Ingredient ID to add"),
    quantity: float = Query(default=None, description="Quantity (optional)"),
    unit: str = Query(default=None, description="Unit (optional)"),
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Add an ingredient to the users inventory.
    """
    # Check if ingredient exists
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    # Check if already in inventory
    existing = db.query(UserInventory).filter(
        UserInventory.user_id == user_id,
        UserInventory.ingredient_id == ingredient_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ingredient already in inventory")
    
    # Add to inventory
    item = UserInventory(
        user_id=user_id,
        ingredient_id=ingredient_id,
        quantity=quantity,
        unit=unit
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "message": "Added to inventory",
        "ingredient": ingredient.name,
        "id": item.id
    }

@router.delete("/{ingredient_id}")
def remove_from_inventory(
    ingredient_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Remove an ingredient from user's inventory
    """
    item = db.query(UserInventory).filter(
        UserInventory.user_id == user_id,
        UserInventory.ingredient_id == ingredient_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not in inventory.")
    
    db.delete(item)
    db.commit()

    return {"message": "Removed from inventory"}

@router.put("/{ingredient_id}")
def update_inventory_item(
    ingredient_id: int,
    quantity: float = Query(..., description="New quantity"),
    unit: str = Query(..., description="New unit"),
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Update quantity/units of an inventory item
    """
    item = db.query(UserInventory).filter(
        UserInventory.user_id == user_id,
        UserInventory.ingredient_id == ingredient_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not in inventory.")
    
    item.quantity = quantity
    item.unit = unit
    db.commit()

    return {"message": "Inventory has been updated."}
