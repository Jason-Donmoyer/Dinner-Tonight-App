from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.recipe import Recipe, RecipeCreate, RecipeMatch
from app.models.recipe import Recipe as RecipeModel, RecipeIngredient, Ingredient
from app.services.matching import RecipeMatchingService

router = APIRouter()

@router.get("/suggestions", response_model=List[RecipeMatch])
def get_recipe_suggestions(
    max_missing: int = Query(default=2, ge=0, le= 5, description="Maximum missing ingredients"),
    limit: int = Query(default=10, ge=1, le=50, description="Number of suggestions to return"),
    db: Session = Depends(get_db)
):
    """
    Get recipe suggestions based on user's ingredient inventory.
    - **max_missing**: Allow recipes with up to this many missing ingredients
    - **limit**: Maximum number of recipes to return
    """
    service = RecipeMatchingService(db)
    return service.find_matching_recipes(
        user_id=1,
        max_missing=max_missing,
        limit=limit
    )

@router.post("/", response_model=Recipe, status_code=201)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Create a new recipe with ingredients
    """
    # Create the recipe
    db_recipe = RecipeModel(
        name=recipe.name,
        description=recipe.description,
        instructions=recipe.instructions,
        cooking_time=recipe.cooking_time,
        servings=recipe.servings
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    # Add recipe ingredients
    for ing in recipe.ingredients:
        recipe_ing = RecipeIngredient(
            recipe_id=db.recipe.id,
            ingredient_id=ing.ingredient_id,
            quantity=ing.quantity,
            unit=ing.unit,
            notes=ing.notes
        )
        db.add(recipe_ing)

    db.commit()
    db.refresh(db_recipe)

    return db_recipe

@router.get("/", response_model=List[Recipe])
def list_recipes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List all recipes with pagination.
    """
    recipes = db.query(RecipeModel).offset(skip).limit(limit).all()
    return recipes

@router.get("/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Get specific recipe by id
    """
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

    