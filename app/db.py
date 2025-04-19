from datetime import date
import os

from typing import Generator, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from .models import Base, Menu, MenuItem, Ingredient, Allergy
from .enums import MealLocation
from .dataclasses import MenuItemData

# Exposed functions and variables
__all__ = ["add_or_update_menu", "create_menu_item_db", "connect_menu_and_menu_items"]

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
print("Database URL: ", DATABASE_URL)
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


def create_menu_item_db(menu_item_obj: MenuItemData) -> MenuItem:

    existing_menu_item = (
        db.query(MenuItem)
        .filter(
            MenuItem.category == menu_item_obj.category,
            MenuItem.name == menu_item_obj.name,
        )
        .first()
    )

    if not existing_menu_item:
        menu_item = MenuItem(
            name=menu_item_obj.name,
            category=menu_item_obj.category,
            serving_size=menu_item_obj.serving_size,
            calories_per_serving=menu_item_obj.calories_per_serving,
            ingredients=menu_item_obj.ingredients,
            allergies=menu_item_obj.allergies,
        )
        db.add(menu_item)
        db.commit()
        return menu_item
    else:
        updated = False

        # Check if a change is detected
        if existing_menu_item.serving_size != menu_item_obj.serving_size:
            existing_menu_item.serving_size = menu_item_obj.serving_size
            updated = True

        # Check if a change is detected
        if (
            existing_menu_item.calories_per_serving
            != menu_item_obj.calories_per_serving
        ):
            existing_menu_item.calories_per_serving = menu_item_obj.calories_per_serving
            updated = True

        # Check if a change is detected
        existing_ings = {ing.ingredient for ing in existing_menu_item.ingredients}
        new_ings = {ing.ingredient for ing in menu_item_obj.ingredients}

        if existing_ings != new_ings:
            existing_menu_item.ingredients = menu_item_obj.ingredients
            updated = True

        # Check if a change is detected
        existing_allergies = {alg.allergy_type for alg in existing_menu_item.allergies}
        new_allergies = {alg.allergy_type for alg in menu_item_obj.allergies}

        if existing_allergies != new_allergies:
            existing_menu_item.allergies = menu_item_obj.allergies
            updated = True

        menu_item = existing_menu_item

        if updated:
            db.add(menu_item)
            db.commit()

        return existing_menu_item


def connect_menu_and_menu_items(menu: Menu, menu_items: List[MenuItem]):
    to_add_menu_items = []
    for menu_item in menu_items:
        if menu_item not in menu.menu_items:
            to_add_menu_items.append(menu_item)

    menu.menu_items.extend(to_add_menu_items)
    db.commit()


def convert_to_ingredient_objects(ingredients: List[str]) -> List[Ingredient]:
    converted_ingredients: List[Ingredient] = []
    existing = db.query(Ingredient).filter(Ingredient.ingredient.in_(ingredients)).all()
    existing_map = {i.ingredient: i for i in existing}

    for ing in ingredients:
        if ing in existing_map:
            converted_ingredients.append(existing_map[ing])
        else:
            new_ing = Ingredient(ingredient=ing)
            db.add(new_ing)
            converted_ingredients.append(new_ing)
    db.commit()
    return converted_ingredients


def convert_to_allergy_objects(allergies: List[str]) -> List[Allergy]:
    converted_allergies: List[Allergy] = []
    existing = db.query(Allergy).filter(Allergy.allergy_type.in_(allergies)).all()
    existing_map = {i.allergy_type: i for i in existing}

    for al in allergies:
        if al in existing_map:
            converted_allergies.append(existing_map[al])
        else:
            new_allergy = Allergy(allergy_type=al)
            db.add(new_allergy)
            converted_allergies.append(new_allergy)
    db.commit()
    return converted_allergies


def get_menu_item(menu_item_obj: MenuItemData) -> "MenuItem | None":
    existing_menu_item = (
        db.query(MenuItem)
        .filter(
            MenuItem.name == menu_item_obj.name,
        )
        .first()
    )
     
    return existing_menu_item
