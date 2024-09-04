#from app.DataBase.classes_of_obj import groups
from db_conn import async_engine
from sqlalchemy import text, Table, MetaData, Column, String, Boolean, Date, SmallInteger, insert, select

import asyncio, logging

#from sqlalchemy import Table, MetaData, Column, String, Boolean, Date, SmallInteger


metadata = MetaData()

students = Table(
    'students',
    metadata,
    Column('id', SmallInteger, primary_key=True),
    Column('first_name', String(50), nullable=False),
    Column('last_name', String(50), nullable=False),
    Column('surname', String(50)),
    Column('is_headman', Boolean, default=False, nullable=False),
    Column('mobile_num', String(12)),
    Column('birthday', Date),
    Column('email', String(250)),
    Column('group_id', SmallInteger),
    Column('tg_nickname', String(50), unique=True, nullable=False)
)

groups = Table(
    'groups',
    metadata,
    Column('group_id', SmallInteger, primary_key=True),
    Column('full_name',String(25), nullable=False),
    Column('short_name',String(8), nullable=False),
    Column('faculty',String(250), nullable=False),
    Column('direction',String(110), nullable=False),
    Column('group_email',String(250)),
    Column('enrollment_year', SmallInteger),
    Column('graduation_year', SmallInteger)
)




async def get_groups():
    async with async_engine.connect() as session:
        stmt = select(groups.c.short_name)
        res = await session.execute(stmt)
        groups_list = res.fetchall()
        print(groups_list)
        return groups_list


async def get_group_by_student():
    async with async_engine.connect() as session:
        #temp = select(students.c.group_id).where(students.c.tg_nickname == nickname)
        #res = await session.execute(temp)
        #group_id= res.fetchone()
        group_id = 1
        stmt = select(groups.c.full_name).where(groups.c.group_id == group_id)
        res = await session.execute(stmt)
        group = res.fetchone()
        print(group)
        return group


# async def get_student_by_nickname(nickname: str):
#     async with async_engine.connect() as session:
#         stmt = select(students).where(students.c.tg_nickname == nickname)
#         res = await session.execute(stmt)
#         student = res.fetchone()
#         print(res.first())
#         return student

asyncio.run(get_groups())
logging.basicConfig(level=logging.INFO)
asyncio.run(get_group_by_student())
