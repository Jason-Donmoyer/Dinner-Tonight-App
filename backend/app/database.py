# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection to string
# Format: postgresql://username:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jasondonmoyer@localhost:5432/recipes"
)

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BAse class for models
Base = declarative_base()

# Dependency for getting database sessions in routes
def get_db():
    """
    Creates a new database session for each request.
    Automatically closes when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


