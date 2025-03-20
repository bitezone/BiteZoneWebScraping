from datetime import date
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from .models import Base, Menu
from .enums import MealLocation

# Exposed functions and variables
__all__ = ["add_or_update_menu"]

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False)
db = SessionLocal()


def add_or_update_menu(
    meal_date_format: date, meal_time_format: str, meal_location: str
) -> None:
    """add or updates menu information into "menus" db

    Parameters
    ----------
    meal_date_format: date
    
    meal_time_format: str
    
    meal_location: str
    - Acceptable strings "Cooper", "Lakeside", "Pathfinder"
    """
    existing_menu = (
        db.query(Menu)
        .filter(
            Menu.date == meal_date_format,
            Menu.meal_time == meal_time_format,
            Menu.meal_location == MealLocation(meal_location),
        )
        .first()
    )

    if not existing_menu:
        menu = Menu(
            date=meal_date_format,
            meal_time=meal_time_format,
            meal_location=MealLocation(meal_location),
        )
        db.add(menu)
        db.commit()
    else:
        print("data already there so no new stuff created")
        

