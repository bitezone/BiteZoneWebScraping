from typing import List
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import relationship, backref, DeclarativeBase, mapped_column, Mapped
from .enums import MealLocation


class Base(DeclarativeBase):
    pass


menu_items_assocation = Table(
    "menu_items_association",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("menu_id", Integer, ForeignKey("menus.id")),
    Column("menu_item_id", Integer, ForeignKey("menu_items.id")),
)

menu_items_allergies_association = Table(
    "menu_items_allergies_association",
    Base.metadata,
    Column("menu_item_id", ForeignKey("menu_items.id")),
    Column("allergy_id", ForeignKey("allergies.id"))
)

# menu_items_ingredients_association = Table(
#     "menu_items_ingredients_association",
#     Base.metadata,
#     Column("menu_item_id", ForeignKey("menu_items.id")),
#     Column("ingredient_id", ForeignKey("ingredients.id"))
# )

class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    meal_time: Mapped[str] = mapped_column(nullable=False)
    meal_location: Mapped[MealLocation] = mapped_column(nullable=False)

    menu_items: Mapped[List["MenuItem"]] = relationship(
        secondary=menu_items_assocation, back_populates="menus"
    )

    def __repr__(self):
        return f"Menu(id={self.id}, date={self.date}, meal_time={self.meal_time}, meal_location={self.meal_location}, menu_items={self.menu_items})"


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    serving_size = Column(String, nullable=True)
    calories_per_serving = Column(Integer, nullable=True)
    

    menus: Mapped[List["Menu"]] = relationship(
        secondary=menu_items_assocation, back_populates="menu_items"
    )
    
    # allergies: Mapped[List["Allergies"]] = relationship(
    #     secondary=menu_items_allergies_association, back_populates="menu_items"
    # )

    def __repr__(self):
        return f"MenuItem(id={self.id}, name={self.name}, category={self.category}), serving_size={self.serving_size}, calories={self.calories_per_serving}"
    
    
# class Allergies(Base):
#     __tablename__ = "allergies"
    
#     id = Column(Integer, primary_key=True)
#     allergy_type = Column(String, nullable=False)
    
#     menu_items: Mapped[List["MenuItem"]] = relationship(
#         secondary=menu_items_allergies_association, back_populates="allergies"
#     )
    
# class Ingredient(Base):
#     __tablename__ = "ingredients"
    
#     id = Column(Integer, primary_key=True)
#     ingredient = Column(String, nullable=False)
    
    
    
