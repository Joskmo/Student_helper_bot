from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from app.DataBase.requests import get_group_by_student
from app.bot.middlewares.schedule_finder import find_schedule


router = Router()


#dictionary for lesson type
lesson_type_dict = {
    'sem': 'Семинар',
    'lect': 'Лекция'
}


def schedule_parser(schedule):
    reply_text = ""
    for i in range(0,6):
        day = schedule[str(i)]
        reply_text += f"Дата: {day['date']}, {day['name']}"
        if day['lessons']:  # Проверяем, есть ли занятия
            for lesson in day['lessons']:
                reply_text += f"""<blockquote><b>Номер пары: </b>{lesson['num']}
<b>Дисциплина: </b>{lesson['name']}
<b>Время: </b>{lesson['time']}
<b>Тип: </b>{lesson_type_dict[lesson['type']]}
<b>Аудитория: </b>{lesson['place']}
</blockquote>"""
        else:
            reply_text += f"<blockquote>Занятий нет</blockquote>"
    
    return reply_text

@router.message(F.text.lower() == "открыть расписание", StateFilter(None))
async def get_schedule(message: Message):
    tg_nickname = message.from_user.username
    group = await get_group_by_student(tg_nickname)
    if group:
        res = await find_schedule(group.full_name, None) # внимание!!! Тут нужно поменять None на текущую неделю. Сиди, сука, и думай
        schedule = res['schedule']
        reply_text = schedule_parser(schedule)
        await message.answer(reply_text)
    else: 
        await message.answer(f'У тебя не указана группа')