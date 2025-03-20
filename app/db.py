from datetime import date
import os
from typing import Generator, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from .models import Base, Menu, MenuItem
from .enums import MealLocation

# Exposed functions and variables
__all__ = ["add_or_update_menu", "create_menu_item_db", "connect_menu_and_menu_items"]

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False)
db = SessionLocal()


def add_or_update_menu(
    meal_date_format: date, meal_time_format: str, meal_location: str
) -> Menu:
    """add or updates menu information into "menus" db
    
    return: Menu - object realated to the parameters

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
        return menu
    else:
        return existing_menu


def create_menu_item_db(category_text: str, menu_item_text: str) -> MenuItem:

    existing_menu_item = db.query(MenuItem).filter(
        MenuItem.category == category_text, MenuItem.name == menu_item_text
    ).first()

    if not existing_menu_item:
        menu_item = MenuItem(name=menu_item_text, category=category_text)
        db.add(menu_item)
        db.commit()
        return menu_item
    else:
        return existing_menu_item

def connect_menu_and_menu_items(menu: Menu, menu_items: List[MenuItem]):
    to_add_menu_items = []
    print(menu)
    for menu_item in menu_items:
        if menu_item not in menu.menu_items:
            to_add_menu_items.append(menu_item)
        
    menu.menu_items.extend(to_add_menu_items)
    db.commit()