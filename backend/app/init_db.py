from app.database import engine, Base
from app.models.recipe import Recipe,Ingredient, RecipeIngredient, UserInventory

def init_db():
    """
    Create all database tables
    """

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    init_db()