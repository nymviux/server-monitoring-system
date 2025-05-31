from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Pobieramy dane z environment variables (które ustawiasz w docker-compose)
DB_USER = os.getenv("DB_USER", "db")
DB_PASSWORD = os.getenv("DB_PASSWORD", "hehe123")
DB_HOST = os.getenv("DB_HOST", "db")  # Nazwa kontenera!
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "monitoring")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
