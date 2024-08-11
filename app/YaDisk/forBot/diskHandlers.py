from aiogram import Router, F, Bot, types
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold, BlockQuote
from app.YaDisk.yaDisk import get_files
from app.YaDisk.forBot import keyboards as kb

router = Router()

import os


@router.message(F.text.lower() == "перейти в файлы")
async def go_to_files(message: Message):
    result = await get_files()
    message_to_user_files = "<b>Список файлов:</b> <blockquote>"
    if result.get('file'):
        for file in result.get('file'):
            message_to_user_files += f'\n{file}'
        # print(result.get('file'))
        message_to_user_files += "</blockquote>"
    else:
        print(f'В данной папке нет файлов')
    await message.answer(f'''{message_to_user_files}''', reply_markup=kb.get_files(result))
    await message.answer('Или выбери папку для перехода:', reply_markup=kb.get_folders(result))
