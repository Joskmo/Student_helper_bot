from sqlalchemy import Table, Column, Integer, String, Boolean, SmallInteger, VARCHAR, DATE, MetaData

metadata_obj = MetaData()


students_table = Table(
    "students",
    metadata_obj,
    Column("id", SmallInteger, primary_key=True),
    Column("first_name", VARCHAR(50), ),
    Column("last_name", VARCHAR(50)),
    Column("is_headman", Boolean, default=False),
    Column("surname", VARCHAR(50)),
    Column("mobile_num", VARCHAR(12)),
    Column("birthday", DATE),
    Column("email", VARCHAR(250)),
    Column("group_id", SmallInteger),
    Column("tg_nickname", VARCHAR(30)),
)