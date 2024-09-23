import requests
import json
import re
import app.bot.middlewares.classes as classes
import string
from bs4 import BeautifulSoup

rasp_dict = {}

# dictionary for timetable (get time by lesson num)
time_dict = {
    1: "08:30 - 10:00",
    2: "10:10 - 11:40",
    3: "12:50 - 13:20",
    4: "14:00 - 15:30",
    5: "15:40 - 17:10",
    6: "17:20 - 18:50",
    7: "18:55 - 20:25", 
    8: "20:30 - 22:00"
}

#dictionary for lesson type
lesson_type_dict = {
    'Практическое занятие': 'sem',
    'Лекция': 'lect',
    'Лабораторная работа': 'lab'
}

# List if days of the week
days_of_week = [
    "ПОНЕДЕЛЬНИК",
    "ВТОРНИК",
    "СРЕДА",
    "ЧЕТВЕРГ",
    "ПЯТНИЦА",
    "СУББОТА"
]

headers = {
    'X-Requested-With': 'XMLHttpRequest',
}

link = "https://rasp.rea.ru/Schedule/ScheduleCard?selection="

def get_schedule(group_dict: dict): 
    # weekNum = 1
    # group_num = "15.27Д-БИ20/22б"
    group_link = link + group_dict['group_num'].lower() + "&weekNum=" + (str(group_dict['week_num']) if group_dict['week_num'] else "")


    response = requests.get(
        # 'https://rasp.rea.ru/Schedule/ScheduleCard?selection=15.27д-би20/22б&weekNum=1',
        group_link,
        headers=headers,
    ).text


    # parse HTML data
    soup = BeautifulSoup(response, 'html.parser')

    tables = soup.find_all('table', class_=['table table-light', 'table table-light today'])
    cur_week = soup.find('input', id='weekNum').get('value')

    for day, day_num in zip(days_of_week, range(0, 6)):
        
        day_table = next((table for table in tables if day in table.find('h5').get_text()), None)
        if day_table:

            date_text = day_table.find('h5').get_text()
            date = date_text.split(', ')[1]
            cur_day = classes.Day(date=date, name=string.capwords(day)) # date

            slots = day_table.find_all('tr', class_='slot load-lecture') + day_table.find_all('tr', class_='slot load-seminar-2') + day_table.find_all('tr', class_='slot load-lab')
            if slots:
                cur_day.lessons = []
                for slot in slots:
                    
                    # info about lesson num(). We need only num of pair -> use regular expression
                    time_info = int(re.match(r'\d', (slot.find('span', class_='pcap').get_text(strip=True)))[0])
                    
                    cur_less = classes.Lesson(num=time_info)
                    cur_less.time = time_dict[time_info]

                    lesson_link = slot.find('a', class_='task')
                    if lesson_link:
                        title = lesson_link.contents[0].strip() # name of lesson
                        cur_less.name = title

                        lesson_type = lesson_type_dict[lesson_link.i.get_text(strip=True)] # type of lesson from dict
                        cur_less.type = lesson_type

                        location_parts = list(lesson_link.stripped_strings)[2]
                        match = re.search(r'(\d+)\s*корпус\s*-\s*([\d/*.]+|[\w/ №\d]+)', location_parts)
                        if match:
                            location = f"{match.group(1)[0]}к {match.group(2)}"
                        else:
                            location = "Неизвестно"
                        cur_less.place = location

                    cur_day.lessons.append(cur_less)
                    
                # sort for classes by num: 
                n = len(cur_day.lessons)
                for i in range(0, n-1):
                    for j in range(0, n-1):
                        if (cur_day.lessons[j].num > cur_day.lessons[j+1].num): 
                            cur_day.lessons[j], cur_day.lessons[j+1] = cur_day.lessons[j+1], cur_day.lessons[j]

            day_dict = cur_day.model_dump()
            rasp_dict[str(day_num)] = day_dict

    # with open('test.json', 'w', encoding='utf-8') as file:
    #     json.dump(rasp_dict, file, indent=4, ensure_ascii=False)

    return rasp_dict, int(cur_week)

if __name__ == "__main__":
    get_schedule({
        'group_num': '15.27д-би20/22б',
        'week_num': None
        })