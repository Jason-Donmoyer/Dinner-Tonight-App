# backend/seed_data.py
"""
Seed the database with initial test data
"""
from app.database import SessionLocal
from app.models.recipe import Recipe, Ingredient, RecipeIngredient, UserInventory

def seed_data():
    db = SessionLocal()
    
    try:
        print("Seeding database with test data...")
        
        # Create ingredients
        print("Creating ingredients...")
        ingredients_data = [
            ("chicken breast", "protein"),
            ("rice", "grain"),
            ("broccoli", "vegetable"),
            ("tomato", "vegetable"),
            ("pasta", "grain"),
            ("olive oil", "fat"),
            ("garlic", "vegetable"),
            ("onion", "vegetable"),
            ("salt", "seasoning"),
            ("pepper", "seasoning"),
        ]
        
        ingredients = {}
        for name, category in ingredients_data:
            # Check if already exists
            existing = db.query(Ingredient).filter(Ingredient.name == name).first()
            if existing:
                ingredients[name] = existing
                print(f"  ✓ {name} already exists")
            else:
                ing = Ingredient(name=name, category=category)
                db.add(ing)
                db.flush()
                ingredients[name] = ing
                print(f"  ✓ Created {name}")
        
        db.commit()
        
        # Create a sample recipe
        print("\nCreating sample recipe...")
        recipe = Recipe(
            name="Simple Chicken and Rice",
            description="A quick and easy chicken and rice dinner",
            instructions="1. Cook rice according to package directions\n2. Season and cook chicken\n3. Steam broccoli\n4. Serve together",
            cooking_time=30,
            servings=4
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        print(f"  ✓ Created recipe: {recipe.name}")
        
        # Link ingredients to recipe
        print("\nLinking ingredients to recipe...")
        recipe_ingredients = [
            (ingredients["chicken breast"], 1.5, "lb", "diced"),
            (ingredients["rice"], 2, "cups", None),
            (ingredients["broccoli"], 2, "cups", "chopped"),
            (ingredients["olive oil"], 2, "tbsp", None),
        ]
        
        for ing, qty, unit, notes in recipe_ingredients:
            ri = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ing.id,
                quantity=qty,
                unit=unit,
                notes=notes
            )
            db.add(ri)
            print(f"  ✓ Added {ing.name}")
        
        db.commit()
        
        # Add items to user inventory
        print("\nAdding items to user inventory...")
        inventory_items = [
            (ingredients["chicken breast"], 2, "lb"),
            (ingredients["rice"], 5, "cups"),
            (ingredients["olive oil"], 1, "cup"),
            (ingredients["salt"], None, None),
            (ingredients["pepper"], None, None),
        ]
        
        for ing, qty, unit in inventory_items:
            # Check if already exists
            existing = db.query(UserInventory).filter(
                UserInventory.user_id == 1,
                UserInventory.ingredient_id == ing.id
            ).first()
            
            if not existing:
                inv = UserInventory(
                    user_id=1,
                    ingredient_id=ing.id,
                    quantity=qty,
                    unit=unit
                )
                db.add(inv)
                print(f"  ✓ Added {ing.name} to inventory")
            else:
                print(f"  ✓ {ing.name} already in inventory")
        
        db.commit()
        
        print("\n✅ Database seeded successfully!")
        print(f"   - {len(ingredients)} ingredients")
        print(f"   - 1 recipe")
        print(f"   - {len(inventory_items)} items in inventory")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()