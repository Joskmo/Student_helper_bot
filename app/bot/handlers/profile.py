from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, BlockQuote, Text
from typing import Optional

from app.DataBase.requests import get_group_by_student, get_student_by_nickname
import app.bot.keyboards.keyboards as kb
import app.bot.filters.dateFunctions as dateFunc

router = Router()


@router.message(Command("dev_cont"))
async def dev_contact(message: Message):
    content = Text(Bold("Telegram разработчика: @joskmo\n"), '''Пиши с любыми вопросами и предложениями
Сообщение от разработчика:''', BlockQuote("Спасибо, что доверяешь мне, ", message.from_user.first_name,
"\nЯ стараюсь сделать свой проект лучше"))
    await message.answer(**content.as_kwargs())
    await message.answer_sticker(r'CAACAgIAAxkBAAEG26hmkaT1hlBBAWpW5-6IUM1S0IOwMAACAhYAAiV2KEkRdkQ6i8Hv3jUE')


@router.message(F.text.lower() == "мой профиль", StateFilter(None))
async def my_profile(message: Message, tg_nickname: Optional[str] = None):
    if tg_nickname is None: tg_nickname = message.from_user.username
    student = await get_student_by_nickname(tg_nickname)
    if student:
        parsed_bd: str
        if student.birthday is not None:
            birthday = dateFunc.parse_date(student.birthday)
            parsed_bd = f'''{birthday['day']} {birthday['month']} {birthday['year']}'''
        user_data = (
f"""<b>Фамилия:</b> <i>{student.last_name}</i>
<b>Имя:</b> <i>{student.first_name}</i>
<b>Отчество:</b> <i>{student.surname if (student.surname != None) else 'Не указано'}</i>
<b>Мобильный номер:</b> <i>{student.mobile_num if (student.mobile_num != None) else 'Не указано'}</i>
<b>Email:</b> <i>{student.email if (student.email != None) else 'Не указано'}</i>
<b>Дата рождения:</b> <i>{parsed_bd if (student.birthday != None) else 'Не указано'}</i>
<b>Староста:</b> <i>{'Да' if student.is_headman else 'Нет'}</i>"""
)
        await message.answer(f'<b>Твои данные:</b> <blockquote>{user_data}</blockquote>',
                             reply_markup=kb.profile_kb())
    else:
        msg = await message.answer('Обработка...', reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Я тебя не нахожу 🙁\nЖелаешь создать профиль?', reply_markup=kb.create_profile())
        await msg.delete()


@router.callback_query(F.data.startswith('get_group_number'))
async def get_group_num(call: CallbackQuery):
    tg_nickname = call.from_user.username
    group = await get_group_by_student(tg_nickname)
    if group:
        group_data = (
f"""<b>Полное название группы:</b> <i>{group.full_name}</i>
<b>Короткое название:</b> <i>{group.short_name}</i>
<b>Направление:</b> <i>{group.direction}</i>
<b>Высшая школа (факультет):</b> <i>{group.faculty}</i>
<b>Почта твоей группы:</b> <i>{group.group_email}</i>
<b>Староста группы:
    Имя:</b> {group.first_name}
    <b>Фамилия:</b> {group.last_name}
    <b>Telegram: </b>@{group.tg_nickname}"""
    )
        await call.answer(cache_time=5)
        await call.message.edit_text(
            text=f'<b>Информация о твоей группе:</b> <blockquote>{group_data}</blockquote>',
            reply_markup=kb.in_group()
        )
    else:
        await call.answer(cache_time=5)
        await call.message.edit_text(
            f'У тебя не указана группа. Хочешь отправить запрос на добавление в группу?',
            reply_markup=kb.wanna_group()
        )


@router.callback_query(F.data.casefold() == "profile")
async def back(call: CallbackQuery):
    await call.message.delete()
    await my_profile(call.message, call.from_user.username)


@router.callback_query(F.data.casefold() == "no_i_dont")
async def no_i_dont(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.delete()
    await my_profile(message=call.message, tg_nickname=call.from_user.username)
    