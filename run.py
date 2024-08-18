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

from app.bot.handlers import profile, createOrEditProfile, tests, editProfile, addToGroup
from app.YaDisk.forBot import diskHandlers
from app.bot.tokenLoader import config

bots = [
    Bot(
        token=config.tg_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML)),
    Bot(
        token="7408213884:AAERALzfLCmXVyX3YUif1xJA6clKj6TK35I",
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML))
]

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
        addToGroup.router
    )
    await bots[for num in rang].delete_webhook(drop_pending_updates=True)
    await bots


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Только на дебаг
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
