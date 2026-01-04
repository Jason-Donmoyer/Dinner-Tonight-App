from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.database import get_db
from app.schemas.recipe import Ingredient, IngredientCreate
from app.models.recipe import Ingredient as IngredientModel

router = APIRouter()

@router.get("/search")
def search_ingredients(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Search for ingredients by name.
    Returns ingredients that match the search query.
    """
    # Case-intensive search
    search_pattern = f"%{q.lower()}%"

    ingredients = db.query(IngredientModel).filter(
        IngredientModel.name.ilike(search_pattern)
    ).limit(limit).all()

    return [
        {
            "id": ing.id,
            "name": ing.name,
            "category": ing.category
        }
        for ing in ingredients
    ]

@router.post("/", response_model=Ingredient, status_code=201)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """
    Create a new ingredient
    """
    # Check if ingredient already exists
    existing = db.query(IngredientModel).filter(
        IngredientModel.name == ingredient.name.lower()
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ingredient already exists")
    
    db_ingredient = IngredientModel(
        name=ingredient.name.lower(),
        category=ingredient.category
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient

@router.get("/", response_model=List[Ingredient])
def list_ingredients(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    List all ingredients with pagination.
    """
    ingredients = db.query(IngredientModel).offset(skip).limit(limit).all()
    return ingredients