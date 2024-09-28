from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мой профиль")
    kb.button(text="Открыть расписание")
    # kb.button(text="Перейти в файлы")
    kb.button(text="Тут будут ещё функции 😉")
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard = True,
        input_field_placeholder = "Выбери пункт меню",
        one_time_keyboard=True)


def profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Узнать номер группы", callback_data="get_group_number")
    kb.button(text="Редактировать профиль", callback_data="edit_profile")
    kb.button(text="В главное меню", callback_data="to_main_menu")
    kb.adjust(1)
    return kb.as_markup()


def create_profile() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="yes_create")
    kb.button(text="Нет", callback_data="no_create")
    # kb.button(text="Вернуться назад")
    kb.adjust(2)
    return kb.as_markup()


def confirm_data() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="yes_confirm")
    kb.button(text="Нет", callback_data="no_confirm")
    # kb.button(text="Вернуться назад")
    kb.adjust(2)
    return kb.as_markup()


def creating_profile() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="yes_this")
    kb.button(text="Введу все данные вручную", callback_data="no_manual")
    kb.adjust(1)
    return kb.as_markup()


def skip() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пропустить")
    return kb.as_markup(resize_keyboard = True,
        one_time_keyboard=True)


def req_contact() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить контакт", request_contact=True)
    kb.button(text="Пропустить")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard = True,
        one_time_keyboard=True)


def what_to_edit() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Все данные", callback_data="no_manual")
    kb.button(text="Что-то конкретное", callback_data="smth")
    kb.button(text="Вернуться назад", callback_data="profile")
    kb.adjust(1)
    return kb.as_markup()


def edit_pls() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Имя", callback_data="first_name")
    kb.button(text="Фамилия", callback_data="last_name")
    kb.button(text="Отчество", callback_data="surname")
    kb.button(text="Номер телефона", callback_data="mobile_num")
    kb.button(text="День рождения", callback_data="birthday")
    kb.button(text="Email", callback_data="email")
    kb.adjust(2)
    kb.row(
        InlineKeyboardButton(text="Готово", callback_data="ready"),
        InlineKeyboardButton(text="<< Назад", callback_data="back"),
        width=1
    )
    return kb.as_markup()


def in_group() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Сменить группу", callback_data="change_group")
    kb.button(text="Назад", callback_data="profile")
    return kb.as_markup()


def wanna_group() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="change_group")
    kb.button(text="Нет", callback_data="no_i_dont")
    kb.adjust(2)
    return kb.as_markup()


def select_group(group_list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for group_id in group_list:
        kb.button(text=f'{group_id.full_name}', callback_data=f'num_{group_id.group_id}')
    kb.button(text="Назад", callback_data="get_group_number")
    kb.adjust(1)
    return kb.as_markup()


def get_query() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Посмотреть", callback_data="check_query")
    kb.adjust(1)
    return kb.as_markup()


def apply_student(students_list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for student in students_list:
        kb.button(text=f'{student.last_name} {student.first_name}', callback_data=f'accept_{student.tg_nickname}')
    kb.button(text=f'Никого', callback_data="nobody")
    kb.adjust(1)
    return kb.as_markup()


def schedule_navi() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="<<<", callback_data="prev_week")
    kb.button(text=">>>", callback_data="next_week")
    kb.adjust(2)
    kb.row(
        InlineKeyboardButton(text="Ввести номер группы", callback_data="enter_group"),
        InlineKeyboardButton(text="Выйти из расписания", callback_data="sched_exit"),
        width=1
    )
    return kb.as_markup()


def manual_group() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Ввести номер группы", callback_data="enter_group")
    kb.adjust(1)
    return kb.as_markup()


def sched_enter_group() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Выйти из расписания", callback_data="sched_exit")
    kb.adjust(1)
    return kb.as_markup()


def groups_list(group_nums = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if group_nums:
        i = int(0)
        for num in group_nums:
            kb.button(text=num, callback_data="id_" + num)
            i += 1
    kb.button(text="Выход", callback_data="sched_exit")
    kb.adjust(1)
    return kb.as_markup()