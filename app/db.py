import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from .models import Base

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False)
db = SessionLocal()
def get_db() -> Session:
   
    try:
        return db
    finally:
        db.close()
