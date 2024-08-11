import re
from sqlalchemy import Date, String

from datetime import datetime
import app.bot.filters.dateFunctions as dateEdit

pattern_rus = "^[А-Яа-яЁё]+$"
pattern_num = "^[+]+79+[0-9]+$"
pattern_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$|Пропустить'


def rus_str(string):
    pattern = re.compile(pattern_rus)
    result = (pattern.search(string))
    return result


def mob_num(string):
    pattern = re.compile(pattern_num)
    if len(string) == 12:
        result = (pattern.search(string))
    elif string == "Пропустить":
        result = string
    else:
        result = None
    return result


def valid_date(string: str):
    try:
        if string == "Пропустить":
            result = string
        else:
            result = dateEdit.normalize_date_format(string)
    except:
        result = None
    return result


def is_email(string: str):
    pattern = re.compile(pattern_email)
    result = pattern.search(string)
    return result
