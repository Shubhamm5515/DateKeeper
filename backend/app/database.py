from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.config import settings

# Create database engine with optimized settings
if "sqlite" in settings.DATABASE_URL:
    # SQLite configuration (for local development)
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration (for Supabase/production)
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,              # Number of connections to maintain
        max_overflow=10,          # Max connections beyond pool_size
        pool_pre_ping=True,       # Verify connections before using
        pool_recycle=3600,        # Recycle connections after 1 hour
        echo=False                # Set to True for SQL query logging
    )

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
