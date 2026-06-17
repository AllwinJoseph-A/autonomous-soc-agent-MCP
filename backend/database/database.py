from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# We use SQLite for local rapid development. 
# We will swap the URL to PostgreSQL during Dockerization.
SQLALCHEMY_DATABASE_URL = "sqlite:///./soc_platform.db"

# connect_args={"check_same_thread": False} is only needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()