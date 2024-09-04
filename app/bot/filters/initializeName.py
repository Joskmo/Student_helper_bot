import app.bot.filters.strCheck as check

from aiogram.filters import BaseFilter
from aiogram.types import Message


class isValid(BaseFilter):
    async def __call__(self, message: Message):
        data = check.rus_str(message.text)
        return data


class mobileNum(BaseFilter):
    async def __call__(self, message: Message):
        data = check.mob_num(message.text)
        return data


class date(BaseFilter):
    async def __call__(self, message: Message):
        if message != "Пропустить":
            data = check.valid_date(message.text)
        else:
            print('Пропускаем')
            data = "Пропустить"
        return data


class email(BaseFilter):
    async def __call__(self, message: Message):
        if message != "Пропустить":
            data = check.is_email(message.text)
        else:
            data = "Пропустить"
        return data