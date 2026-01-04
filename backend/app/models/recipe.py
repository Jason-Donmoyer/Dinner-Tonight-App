from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class Recipe(Base):
    """
    Recipes table - stores recipe information
    """
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    instructions = Column(Text)
    cooking_time = Column(Integer)
    servings = Column(Integer)

    # Relationship: one recipe has many recipe_ingredients
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class Ingredient(Base):
    """
    Master ingredients table - stores unique ingredient names
    """
    __tablename__ = "ingredients"

    id= Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50)) # e.g. "protien", "vegetable", "spice"


class RecipeIngredient(Base):
    """
    Junction table linking recipes to ingredients with quantities
    """
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Numeric(10, 2)) # e.g., 2.5
    unit = Column(String(20)) # e.g., "cups", "tbsp"
    notes = Column(String(100)) # e.g., "diced", "minced"

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient")


class UserInventory(Base):
    """
    User's ingredient inventory - what thwy currently have
    """
    __tablename__ = "user_inventory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Numeric(10, 2))
    unit = Column(String(20))

    # Relationship
    ingredient = relationship("Ingredient")