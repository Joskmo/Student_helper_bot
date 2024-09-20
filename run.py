import asyncio
import logging

import app.bot.keyboards.keyboards as kb

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils.formatting import Text
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from app.bot.handlers import profile, createOrEditProfile, tests, editProfile, addToGroup, schedule
from app.YaDisk.forBot import diskHandlers
from app.bot.tokenLoader import config

bot = Bot(
        token=config.tg_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML))

dp = Dispatcher()


@dp.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message):
    content = Text("Привет, ", message.from_user.first_name, "!")
    await message.answer(**content.as_kwargs(), reply_markup=kb.main_kb())



async def main():
    dp.include_routers(
        profile.router,
        createOrEditProfile.router,
        tests.router,
        diskHandlers.router,
        editProfile.router,
        addToGroup.router,
        schedule.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Только на дебаг
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
