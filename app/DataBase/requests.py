from app.DataBase.database import async_engine
from sqlalchemy import insert, select, and_, update
from app.DataBase.classes_of_obj import students, groups, Students, Groups


async def get_student_by_nickname(nickname: str):
    async with async_engine.connect() as session:
        stmt = select(students).where(students.c.tg_nickname == nickname)
        res = await session.execute(stmt)
        await session.commit()
        student = res.fetchone()
        return student


async def get_group_by_student(nickname: str):
    async with async_engine.connect() as connection:
        async with connection.begin():
            user = await get_student_by_nickname(nickname)
            if user and user.group_id:
                subq = (
                    select(Students.group_id)
                    .where(Students.tg_nickname == nickname)
                    .scalar_subquery()
                )
                result = await connection.execute(
                    select(
                        Groups.full_name,
                        Groups.short_name,
                        Groups.direction,
                        Groups.faculty,
                        Groups.group_email,
                        Groups.group_id,
                        Students.first_name,
                        Students.last_name,
                        Students.tg_nickname
                    )
                    .join(Groups, Groups.group_id == Students.group_id)
                    .where(
                        and_(
                            Students.is_headman == True,
                            Students.group_id == subq
                        )
                    )
                )
                group_data = result.first()
            else:
                group_data = None
            await connection.commit()
            return group_data


async def add_student(student_dict, nickname: str, id: str):
    async with async_engine.connect() as session:
        check = await get_group_by_student(nickname)
        if check:
            stmt = (
                update(students)
                .where(students.c.tg_nickname == nickname)
                .values(
                    first_name=student_dict['first_name'],
                    last_name=student_dict['last_name'],
                    surname=student_dict['surname'],
                    mobile_num=student_dict['mobile_num'],
                    birthday=student_dict['birthday'],
                    email=student_dict['email'],
                    chat_id=id
                )
            )
        else:
            stmt = (
                insert(students).
                values(
                    first_name=student_dict['first_name'],
                    last_name=student_dict['last_name'],
                    surname=student_dict['surname'],
                    is_headman=False,
                    mobile_num=student_dict['mobile_num'],
                    birthday=student_dict['birthday'],
                    email=student_dict['email'],
                    tg_nickname=nickname,
                    chat_id=id
                )
            )
        await session.execute(stmt)
        await session.commit()


async def get_groups():
    async with async_engine.connect() as session:
        stmt = select(
            groups.c.group_id,
            groups.c.full_name
        )
        res = await session.execute(stmt)
        await session.commit()
        groups_list = res.fetchall()
        return groups_list


async def add_to_query(group_id: int, chat_id: str, tg_nickname: str):
    async with async_engine.connect() as session:
        stmt = (
            update(students)
            .where(students.c.tg_nickname == tg_nickname)
            .values(
                chat_id=chat_id,
                req_group=group_id
            )
        )
        await session.execute(stmt)
        await session.commit()


async def get_headman_by_group_id(group_id: int):
    async with async_engine.connect() as session:
        stmt = (
            select(students.c.chat_id)
            .where(
                and_(
                    students.c.group_id == group_id,
                    students.c.is_headman == True
                )
            )
        )
        res = await session.execute(stmt)
        await session.commit()
        return res.first()


async def get_query(tg_nickname: str):
    res = await get_group_by_student(tg_nickname)
    async with async_engine.connect() as session:
        stmt = (
            select(
                students.c.first_name,
                students.c.last_name,
                students.c.tg_nickname,
                students.c.chat_id
            )
            .where(students.c.req_group == res.group_id)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchall()


async def accept_from_query(tg_nickname: str):
    async with async_engine.connect() as session:
        subq = (
            select(students.c.req_group)
            .where(students.c.tg_nickname == tg_nickname)
            .scalar_subquery()
        )
        await session.execute(
            update(students)
            .where(students.c.tg_nickname == tg_nickname)
            .values(
                group_id = subq,
                req_group = None
            )
        )
        await session.commit()


async def get_chat_id_by_nickname(tg_nickname: str):
    async with async_engine.connect() as session:
        stmt = (
            select(students.c.chat_id)
            .where(students.c.tg_nickname == tg_nickname)
        )
        res = await session.execute(stmt)
        await session.commit()
        return res.fetchone()
