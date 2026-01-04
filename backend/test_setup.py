# backend/test_setup.py
"""
Test script to verify database setup, models, and schemas are working
"""
from app.database import engine, SessionLocal, Base
from app.models.recipe import Recipe, Ingredient, RecipeIngredient, UserInventory
from app.schemas.recipe import IngredientCreate, RecipeCreate, RecipeIngredientCreate
from sqlalchemy import text

def cleanup_test_data():
    """Clean up any existing test data"""
    db = SessionLocal()
    try:
        # Delete in correct order due to foreign keys
        db.query(UserInventory).delete()
        db.query(RecipeIngredient).delete()
        db.query(Recipe).delete()
        db.query(Ingredient).delete()
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def test_database_connection():
    """Test 1: Can we connect to the database?"""
    print("=" * 60)
    print("TEST 1: Database Connection")
    print("=" * 60)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_create_tables():
    """Test 2: Can we create tables?"""
    print("\n" + "=" * 60)
    print("TEST 2: Create Database Tables")
    print("=" * 60)
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Show what tables were created
        with engine.connect() as conn:
            if 'postgresql' in str(engine.url):
                result = conn.execute(text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
            else:  # SQLite
                result = conn.execute(text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table'
                """))
            
            tables = [row[0] for row in result]
            print(f"   Tables created: {', '.join(tables)}")
        return True
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def test_insert_data():
    """Test 3: Can we insert data using models?"""
    print("\n" + "=" * 60)
    print("TEST 3: Insert Test Data")
    print("=" * 60)

    # Clean up any existing test data first
    cleanup_test_data()
    
    db = SessionLocal()
    try:
        # Create test ingredients
        print("   Creating test ingredients...")
        chicken = Ingredient(name="chicken breast", category="protein")
        rice = Ingredient(name="rice", category="grain")
        broccoli = Ingredient(name="broccoli", category="vegetable")
        
        db.add_all([chicken, rice, broccoli])
        db.commit()
        db.refresh(chicken)
        db.refresh(rice)
        db.refresh(broccoli)
        print(f"   ✅ Created ingredients: {chicken.name}, {rice.name}, {broccoli.name}")
        
        # Create test recipe
        print("   Creating test recipe...")
        recipe = Recipe(
            name="Chicken and Rice",
            description="Simple chicken and rice dish",
            instructions="1. Cook rice\n2. Cook chicken\n3. Steam broccoli\n4. Combine",
            cooking_time=30,
            servings=4
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        print(f"   ✅ Created recipe: {recipe.name} (ID: {recipe.id})")
        
        # Link ingredients to recipe
        print("   Linking ingredients to recipe...")
        recipe_ing1 = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=chicken.id,
            quantity=1,
            unit="lb",
            notes="diced"
        )
        recipe_ing2 = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=rice.id,
            quantity=2,
            unit="cups"
        )
        recipe_ing3 = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=broccoli.id,
            quantity=1,
            unit="cup",
            notes="chopped"
        )
        
        db.add_all([recipe_ing1, recipe_ing2, recipe_ing3])
        db.commit()
        print("   ✅ Linked 3 ingredients to recipe")
        
        # Add ingredients to user inventory
        print("   Adding ingredients to user inventory...")
        inv1 = UserInventory(user_id=1, ingredient_id=chicken.id, quantity=2, unit="lb")
        inv2 = UserInventory(user_id=1, ingredient_id=rice.id, quantity=5, unit="cups")
        
        db.add_all([inv1, inv2])
        db.commit()
        print("   ✅ Added 2 ingredients to user inventory")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Data insertion failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_query_data():
    """Test 4: Can we query data?"""
    print("\n" + "=" * 60)
    print("TEST 4: Query Data")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Query recipes
        recipes = db.query(Recipe).all()
        print(f"   Found {len(recipes)} recipe(s)")
        for recipe in recipes:
            print(f"   - {recipe.name}: {len(recipe.ingredients)} ingredients")
        
        # Query ingredients
        ingredients = db.query(Ingredient).all()
        print(f"   Found {len(ingredients)} ingredient(s)")
        for ing in ingredients:
            print(f"   - {ing.name} ({ing.category})")
        
        # Query user inventory
        inventory = db.query(UserInventory).all()
        print(f"   User inventory has {len(inventory)} item(s)")
        for item in inventory:
            print(f"   - {item.ingredient.name}: {item.quantity} {item.unit}")
        
        print("   ✅ All queries successful!")
        return True
        
    except Exception as e:
        print(f"   ❌ Query failed: {e}")
        return False
    finally:
        db.close()

def test_pydantic_schemas():
    """Test 5: Can we use Pydantic schemas?"""
    print("\n" + "=" * 60)
    print("TEST 5: Pydantic Schemas Validation")
    print("=" * 60)
    
    try:
        # Test IngredientCreate schema
        ing_data = IngredientCreate(name="tomato", category="vegetable")
        print(f"   ✅ IngredientCreate: {ing_data.name}")
        
        # Test RecipeIngredientCreate schema
        recipe_ing_data = RecipeIngredientCreate(
            ingredient_id=1,
            quantity=2.5,
            unit="cups",
            notes="diced"
        )
        print(f"   ✅ RecipeIngredientCreate: {recipe_ing_data.quantity} {recipe_ing_data.unit}")
        
        # Test RecipeCreate schema
        recipe_data = RecipeCreate(
            name="Pasta Marinara",
            description="Classic pasta dish",
            cooking_time=20,
            servings=2,
            ingredients=[recipe_ing_data]
        )
        print(f"   ✅ RecipeCreate: {recipe_data.name} with {len(recipe_data.ingredients)} ingredient(s)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Schema validation failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪" * 30)
    print("TESTING DATABASE SETUP")
    print("🧪" * 30 + "\n")
    
    results = []
    
    # Run tests in order
    results.append(("Database Connection", test_database_connection()))
    
    if results[-1][1]:  # Only continue if connection worked
        results.append(("Create Tables", test_create_tables()))
        results.append(("Insert Data", test_insert_data()))
        results.append(("Query Data", test_query_data()))
        results.append(("Pydantic Schemas", test_pydantic_schemas()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nPassed: {total_passed}/{len(results)}")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Your setup is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    run_all_tests()