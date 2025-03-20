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
    Column("menu_id", Integer, ForeignKey("menus.id"), primary_key=True),
    Column("menu_item_id", Integer, ForeignKey("menu_items.id"), primary_key=True),
)


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

    menus: Mapped[List["Menu"]] = relationship(
        secondary=menu_items_assocation, back_populates="menu_items"
    )

    def __repr__(self):
        return f"MenuItem(id={self.id}, name={self.name}, description={self.category})"
