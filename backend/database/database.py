from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv()
# Create SQLite engine
SQLITE_URL = os.getenv("SQLITE_URL")  # or any other path you want
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

# Create session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
