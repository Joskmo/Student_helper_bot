import app.bot.keyboards.keyboards as kb
import app.bot.filters.strCheck as check
import app.bot.filters.initializeName as init
import app.bot.filters.dateFunctions as dateFunc
import app.DataBase.requests as db

import string

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold, BlockQuote
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.engine.row import Row


router = Router()


class EditProfile(StatesGroup):
    choosing_data = State()
    indicating_data = State()
    confirm = State()


@router.callback_query(F.data.startswith('edit_profile'), StateFilter(None))
async def edit_profile(call: CallbackQuery):
    tg_nickname = call.from_user.username
    student = await db.get_student_by_nickname(tg_nickname)
    parsed_bd: str
    if student.birthday != None:
        birthday = dateFunc.parse_date(student.birthday)
        parsed_bd = f'''{birthday['day']} {birthday['month']} {birthday['year']}'''
    user_data = f"""
<b>Фамилия:</b> <i>{student.last_name}</i>
<b>Имя:</b> <i>{student.first_name}</i>
<b>Отчество:</b> <i>{student.surname if (student.surname is not None) else 'Не указано'}</i>
<b>Мобильный номер:</b> <i>{student.mobile_num if (student.mobile_num is not None) else 'Не указано'}</i>
<b>Email:</b> <i>{student.email if (student.email is not None) else 'Не указано'}</i>
<b>Дата рождения:</b> <i>{parsed_bd if (student.birthday is not None) else 'Не указано'}</i>
<b>Староста:</b> <i>{'Да' if student.is_headman else 'Нет'}</i> """
    await call.message.edit_text(f'<b>Текущие данные:</b><blockquote>{user_data}</blockquote>Что будем менять?', 
                                 reply_markup=kb.what_to_edit())
    await call.answer(cache_time=5)


@router.callback_query(F.data.startswith('smth'), StateFilter(None))
async def choose(call: CallbackQuery, state: FSMContext):
    await call.answer(f'Данная функция находится в разработке. Изменить данные можно с помощью другой кнопки')
    # await state.set_state(EditProfile.choosing_data)
    # await call.message.edit_text(f'Выбери данные для изменения:', reply_markup=kb.edit_pls())
    await call.answer(cache_time=5)


@router.callback_query(F.data.startswith('back'), EditProfile.choosing_data)
async def get_back(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await edit_profile(call, state)
