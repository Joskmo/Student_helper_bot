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
from run import bot


router = Router()


@router.callback_query(F.data == "change_group")
async def get_group_list(call: CallbackQuery):
    group_list = await db.get_groups()
    await call.message.edit_text(f'Выбери группу:', reply_markup=kb.select_group(group_list))


@router.callback_query(F.data.startswith("num_"))
async def choose_group_num(call: CallbackQuery):
    chat_id = str(call.message.chat.id)
    tg_nickname = str(call.from_user.username)
    group_id = int(call.data.replace("num_",""))
    await db.add_to_query(group_id, chat_id, tg_nickname)
    headman_id = (await db.get_headman_by_group_id(group_id)).chat_id
    await call.message.edit_text(f'Запрос на добавление в группу отправлен')
    await bot.send_message(headman_id, f'Есть запросы на вступление в группу', reply_markup=kb.get_query())


@router.callback_query(F.data == "check_query")
async def check_query(call: CallbackQuery):
    query = await db.get_query(call.from_user.username)
    reply = "Список студентов:\n"
    counter = 0
    for student in query:
        counter += 1
        reply += f'''Студент №{counter}:
<blockquote>Имя: {student.first_name}
Фамилия: {student.last_name}
Telegram: @{student.tg_nickname}</blockquote>'''
    reply += "\nКого принимаем?"
    await call.message.edit_text(reply, reply_markup=kb.apply_student(query))


@router.callback_query(F.data.startswith("accept_"))
async def accept_student(call: CallbackQuery):
    student_nickname = str(call.data.replace("accept_", ""))
    chat_id = await db.get_chat_id_by_nickname(student_nickname)
    await db.accept_from_query(student_nickname)
    await call.message.edit_text(f'Студент принят в группу', reply_markup=kb.get_query())
    await bot.send_message(chat_id.chat_id, f'Тебя приняли в группу! 😊')


@router.callback_query(F.data == "nobody")
async def no_one_to_accept(call: CallbackQuery):
    await call.message.edit_text(f'Есть запросы на вступление в группу', reply_markup=kb.get_query())
