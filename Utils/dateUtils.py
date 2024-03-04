from datetime import datetime


def get_formatted_date(date:str, format='%d-%m-%Y') -> str:
    if date is None:
        return None
    
    
    try:
        return datetime.strptime(date, format).strftime(format)
    except ValueError:
        return datetime.strptime(date, '%Y-%m-%d').strftime(format)

    