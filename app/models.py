from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref, DeclarativeBase
from .enums import MealTime, MealLocation


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

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    meal_time = Column(Enum(MealTime), nullable=False)
    meal_location = Column(Enum(MealLocation), nullable=False)

    menu_items = relationship(
        "MenuItem", secondary=menu_items_assocation, backref=backref("menus")
    )

    def __repr__(self):
        return f"Menu(id={self.id}, date={self.date}, meal_time={self.meal_time}, meal_location={self.meal_location})"


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"MenuItem(id={self.id}, name={self.name}, description={self.category})"
