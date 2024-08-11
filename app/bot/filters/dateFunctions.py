from datetime import date, datetime

month_dict = {
    '1': 'Января', '2': 'Февраля', '3': 'Марта',
    '4': 'Апреля', '5': 'Мая', '6': 'Июня',
    '7': 'Июля', '8': 'Августа', '9': 'Сентября',
    '10': 'Октября', '11': 'Ноября', '12': 'Декабря'
}


def normalize_date_format(date_str: str):
    formats_to_check = ['%d-%m-%Y', '%Y-%m-%d', '%d.%m.%Y', '%Y.%m.%d']
    for format_str in formats_to_check:
        try:
            date_obj = datetime.strptime(date_str, format_str)
            return date_obj
        except ValueError:
            continue


def parse_date(date: date):
    day = f'{date.day}'
    month = f'''{month_dict[f'{date.month}']}'''
    year = f'{date.year}'
    return {
        'day': day,
        'month': month,
        'year': year
    }

