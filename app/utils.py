
from datetime import date, datetime


def convert_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%B %d").date().replace(year=date.today().year)
