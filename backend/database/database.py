from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create SQLite engine
SQLITE_URL = "sqlite:///./app.db"  # or any other path you want
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

# Create session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
