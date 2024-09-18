import requests, bs4

import app.bot.middlewares.schedule_mongo as mongo
import app.bot.middlewares.classes as classes
import app.bot.middlewares.parser as parser


link = "https://rasp.rea.ru/Schedule/ScheduleCard?selection="


async def find_schedule(group_name: str, week_num):
    result = await mongo.get_schedule(group_name, week_num)
    if (not result):
        group_dict = {
            'group_num': group_name,
            'week_num': week_num
        }
        Schedule = classes.Schedule(group=group_name, week_number=week_num)
        Schedule.schedule, Schedule.week_number = parser.get_schedule(group_dict)
        result = Schedule.model_dump()
        await mongo.add_schedule(result)
    
    return result


def find_week(group_name: str):
    headers = {'X-Requested-With': 'XMLHttpRequest'}

    group_link = link + group_name.lower()
    response = requests.get(group_link, headers=headers).text
    soup = bs4.BeautifulSoup(response, 'html.parser')

    if soup.find('div'): cur_week = int(soup.find('input', id='weekNum').get('value'))
    else: cur_week = None

    return cur_week


def validate_group(group_name: str):
    headers = {'X-Requested-With': 'XMLHttpRequest'}

    group_link = link + group_name.lower()
    response = requests.get(group_link, headers=headers)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    return True if soup.find('div') else False