from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from app.DataBase.requests import get_group_by_student
from app.bot.middlewares.schedule_finder import find_schedule, find_week


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

@router.message(F.text.lower() == "открыть расписание", StateFilter(None))
async def get_schedule(message: Message):
    tg_nickname = message.from_user.username
    group = await get_group_by_student(tg_nickname)
    if group:
        # need to check if the gorup is relevant and schedule exists
        week_num = find_week(group.full_name)
        if week_num:
            res = await find_schedule(group.full_name, week_num)
            reply_text = f"<b>Расписание на неделю №{res['week_number']}</b>\n" + schedule_parser(res['schedule'])
            await message.answer(reply_text)
        else: await message.answer(f'Для указанной группы не найдено расписание. Проверь корректность данных')
    else: 
        await message.answer(f'У тебя не указана группа')
