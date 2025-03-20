
from datetime import date, datetime

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
