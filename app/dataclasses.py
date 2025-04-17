from dataclasses import dataclass

@dataclass
class MenuItemData:
    name: str = ""
    category: str = ""
    serving_size: str = ""
    calories_per_serving: int = -1
    