from aiogram import Router, F, Bot, types
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold, BlockQuote
from app.YaDisk.yaDisk import get_files

router = Router()


@router.message(F.text.lower() == "перейти в файлы")
async def go_to_files(message: Message):
    result = await get_files()
    await message.answer(f'''{result.get('dir')}''')