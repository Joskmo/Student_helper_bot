from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import Table, MetaData, Column, String, Boolean, Date, SmallInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# from database import Base


# class StudentsOrm(Base):
#     __tablename__ = "students"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     first_name: Mapped[str] = mapped_column(nullable=False)
#     last_name: Mapped[str] = mapped_column(nullable=False)
#     surname: Mapped[str]



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
    Column('tg_nickname', String(50), unique=True, nullable=False),
    Column('chat_id', String(15), unique=True),
    Column('req_group', SmallInteger)
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


Base = declarative_base()

class Groups(Base):
    __tablename__ = 'groups'
    group_id = Column(SmallInteger, primary_key=True)
    full_name = Column(String(25))
    short_name = Column(String(8))
    faculty = Column(String(250))
    direction = Column(String(100))
    group_email = Column(String(250))
    enrollment_year = Column(SmallInteger)
    graduation_year = Column(SmallInteger)

class Students(Base):
    __tablename__ = 'students'
    student_id = Column(SmallInteger, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    tg_nickname = Column(String)
    is_headman = Column(Boolean)
    group_id = Column(SmallInteger, ForeignKey('groups.group_id'))


class CreateProfile(StatesGroup):
    yes_create = State()
    no_crate = State()