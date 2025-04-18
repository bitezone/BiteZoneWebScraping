
from datetime import date, datetime
import re

def convert_to_date(date_str: str) -> date:
    """ conversion of String date into date type

    Parameters
    ----------
    date_str: str
    Expected string examples - "March 12", "April 21"
    
    Return
    ---------- 
    date
    """
    return datetime.strptime(date_str, "%B %d").date().replace(year=date.today().year)


def split_ingredients(raw: str) -> list[str]:
    ingredients = []
    buffer = ''
    depth = 0

    for char in raw:
        if char == '(':
            depth += 1
            buffer += char
        elif char == ')':
            depth -= 1
            buffer += char
        elif char == ',' and depth == 0:
            ingredients.append(buffer.strip())
            buffer = ''
        else:
            buffer += char

    if buffer:
        ingredients.append(buffer.strip())

    ingredients = [re.sub(r'\s+', ' ', ing.replace('\xa0', ' ')).strip() for ing in ingredients]
    return ingredients