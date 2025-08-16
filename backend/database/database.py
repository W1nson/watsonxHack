from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv()

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to the database file
db_path = os.path.join(current_dir, "app.db")
SQLITE_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

# Create session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)