from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import recipes, ingredients, inventory

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Dinner Tonight! API",
    description="App for matching recipes to your ingredient inventory",
    version="1.0.0"
)

# Config CORS - allows frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Frontend dev server (nginx)
        "http://localhost:5173",    # Vite dev server
        "http://localhost:8080",    # Alternative Frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)

# Include routers
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["ingredients"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])

@app.get("/")
def read_root():
    """Root endpoint - API info"""
    return {
        "message": "Dinner Tonight! API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"ststus": "healthy"}
