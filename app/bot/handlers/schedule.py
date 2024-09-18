from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.DataBase.requests import get_group_by_student
from app.bot.middlewares.schedule_finder import find_schedule, find_week, validate_group

import app.bot.keyboards.keyboards as kb


router = Router()


#dictionary for lesson type
lesson_type_dict = {
    'sem': 'Семинар',
    'lect': 'Лекция',
    'lab':  'Лабораторная работа'
}


def schedule_parser(schedule):
    reply_text = ""
    for i in range(0,6):
        day = schedule[str(i)]
        reply_text += f"""----------------------------------------------
Дата: {day['date']}, {day['name']}"""
        if day['lessons']:  # Проверяем, есть ли занятия
            for index, lesson in enumerate(day['lessons']):
                reply_text += f"""<blockquote><b>Номер пары: </b>{lesson['num']}
<b>Дисциплина: </b>{lesson['name']}
<b>Время: </b>{lesson['time']}
<b>Тип: </b>{lesson_type_dict[lesson['type']]}
<b>Аудитория: </b>{lesson['place']}</blockquote>"""
                if index != len(day['lessons']) - 1: reply_text += '\n'
        else:
            reply_text += f"<blockquote>Занятий нет</blockquote>"
    
    return reply_text


class ScheduleState(StatesGroup):
    group_name = State()
    week_num = State()
    entering_group = State()


@router.message(F.text.lower() == "открыть расписание")
async def get_schedule(message: Message, state: FSMContext):
    tg_nickname = message.from_user.username
    group = await get_group_by_student(tg_nickname)
    if group:
        # need to check if the gorup is relevant and schedule exists
        week_num = find_week(group.full_name)
        if week_num:
            res = await find_schedule(group.full_name, week_num)
            reply_text = f"<b>Расписание для группы </b>{group.full_name}\n<b>Неделя №{res['week_number']}</b>\n" + schedule_parser(res['schedule'])
            await state.update_data(week_num=res['week_number'], group_name = group.full_name)
            await message.answer(reply_text, reply_markup=kb.schedule_navi())
            await state.set_state(ScheduleState.week_num)
        else: 
            await message.answer(f'Для указанной группы не найдено расписание. Проверь корректность данных', reply_markup=kb.manual_group())
    else: 
        await message.answer(f'У тебя не указана группа', reply_markup=kb.manual_group())
        await state.set_state(ScheduleState.week_num)


@router.callback_query(lambda c: c.data in ['prev_week', 'next_week'], ScheduleState.week_num)
async def week_change(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    week_number = user_data.get('week_num')
    group_name = user_data.get('group_name')
    if call.data == "prev_week": 
        week_number -= 1
    elif call.data == "next_week":
        week_number += 1

    await state.update_data(week_num = week_number)
    res = await find_schedule(group_name, week_number)
    reply_text = f"<b>Расписание для группы </b>{group_name}\n<b>Неделя №{res['week_number']}</b>\n" + schedule_parser(res['schedule'])
    await call.message.edit_text(reply_text, reply_markup=kb.schedule_navi())
    await call.answer(cache_time=1)


@router.message(ScheduleState.week_num)
async def error(message: Message):
    await message.answer("Выбери пункт из меню под сообщением")


@router.callback_query(F.data.casefold() == 'sched_exit', StateFilter(ScheduleState)) 
async def exit_schedule(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer("Выбери пункт меню", reply_markup=kb.main_kb())
    await call.answer(cache_time=1)


@router.callback_query(F.data.casefold() == "enter_group", ScheduleState.week_num)
async def sched_other_group(call: CallbackQuery, state: FSMContext):
    # нужна валидация группы
    await state.clear()
    await state.set_state(ScheduleState.entering_group)
    await call.message.edit_text(
        "Введите полный номер группы или воспользуйтесь кнопкой ниже для поиска", 
        reply_markup=kb.sched_enter_group()
    )
    await call.answer(cache_time=1)


@router.message(ScheduleState.entering_group)
async def enterging_group(message: Message, state: FSMContext):
    data = message.text.lower()
    if validate_group(data):
        week_num = find_week(data)
        await state.update_data(group_name=data)
        res = await find_schedule(data, week_num)
        reply_text = (
            f"<b>Расписание для группы </b>{data}\n <b>Неделя №{res['week_number']}</b>\n" + 
            schedule_parser(res['schedule'])
            )
        await state.update_data(week_num=res['week_number'], group_name = data)
        await message.answer(reply_text, reply_markup=kb.schedule_navi())
        await state.set_state(ScheduleState.week_num)
    else:
        await message.answer("Группа не найдена. Проверь введённые данные")