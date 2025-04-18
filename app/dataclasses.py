from dataclasses import dataclass, field
from typing import List
from .db import Ingredient

@dataclass
class MenuItemData:
    name: str = ""
    category: str = ""
    serving_size: str = ""
    calories_per_serving: int = -1
    ingredients: List[Ingredient] = field(default_factory=list)