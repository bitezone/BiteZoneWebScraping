import os
from sqlalchemy import create_engine
from models import Base


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)