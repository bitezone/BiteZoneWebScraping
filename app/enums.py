import enum

class MealTime(enum.Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"


class MealLocation(enum.Enum):
    COOPER = "Cooper"
    LAKESIDE = "Lakeside"
    PATHFINDER = "Pathfinder"