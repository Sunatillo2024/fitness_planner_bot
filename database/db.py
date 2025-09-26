import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# .env faylda DATABASE_URL ni o‘zgartirsa bo‘ladi
# Misollar:
# sqlite:  DATABASE_URL=sqlite:///./fitness.db
# postgres: DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/fitness_db

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitness.db")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
