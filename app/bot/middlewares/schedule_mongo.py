import motor.motor_asyncio
import app.bot.middlewares.classes

# Connection to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client['university_schedule']  # Название базы данных
collection = database['schedules']        # Название коллекции


async def add_schedule(schedule):
    result = await collection.insert_one(schedule)
    print(f'Расписание добавлено с ID: {result.inserted_id}')


async def get_schedule(group_name, week_number):
    schedule = await collection.find_one({"group": group_name, "week_number": week_number})

    return schedule


# not used yet
async def update_schedule(group_name, week_number, new_subject):
    await collection.update_one(
        {"group": group_name, "week_number": week_number},
        {"$set": {"schedule.0.classes.0.subject": new_subject}}  # Пример обновления
    )
    print(f'Расписание для {group_name} на неделю {week_number} обновлено.')

# not used yet
async def delete_schedule(group_name, week_number):
    await collection.delete_one({"group": group_name, "week_number": week_number})
    print(f'Расписание для {group_name} на неделю {week_number} удалено.')
