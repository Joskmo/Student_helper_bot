import asyncio
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_files(list: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    file_num = 1
    files = list['file']
    print(files)
    for file in files:
        print(file_num)
        kb.button(text=f'{file}', callback_data=f'file_num')
        file_num += 1
    kb.adjust(1)
    return kb.as_markup()


def get_folders(list: dict) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    folders = list['dir']
    for folder in folders:
        kb.button(text=f'{folder}')
    kb.button(text=f'Назад')
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard = True,
        input_field_placeholder='Выбери папку')