from app.bot.middlewares.schedule_mongo import get_schedule, add_schedule
import app.bot.middlewares.classes as classes
import app.bot.middlewares.parser as parser
import json

async def find_schedule(group_name: str, week_num):
    result = await get_schedule(group_name, week_num)
    if (not result):
        group_dict = {
            'group_num': group_name,
            'week_num': week_num
        }
        schedule = classes.Schedule(group=group_name)
        schedule.schedule = parser.get_schedule(group_dict)
        result = schedule_dict = schedule.model_dump()
    
    return result
