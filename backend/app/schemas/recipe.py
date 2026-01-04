from pydantic import BaseModel
from typing import List, Optional

# Ingredient schemas
class IngredientBase(BaseModel):
    name: str
    category: Optional[str] = None

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True # Allows conversion from SQLAlchemy models

# Recipe ingredient schemas
class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredient(RecipeIngredientBase):
    id: int

    class Config:
        from_attributes = True

# Recipe schemas
class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    cooking_time: Optional[int] = None
    servings: Optional[int] = None

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = []

class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True

# Recipe match results (for suggestions)
class RecipeMatch(BaseModel):
    id: int
    name: str
    description: Optional[str]
    cooking_time: Optional[int]
    total_ingredients: int
    matched_ingredients: int
    missing_count: int
    match_percent: float
    missing_ingredients: List[str]

# Inventory schemas
class InventoryItem(BaseModel):
    id: int
    ingredient: str
    ingredient_id: int
    quantity: Optional[float]
    unit: Optional[str]
