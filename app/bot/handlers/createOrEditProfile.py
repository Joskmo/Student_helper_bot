import app.bot.keyboards.keyboards as kb
import app.bot.filters.strCheck as check
import app.bot.filters.initializeName as init
import app.bot.filters.dateFunctions as dateFunc
import app.DataBase.requests as db

import string

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold, BlockQuote
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


router = Router()

class CreateProfile(StatesGroup):
    indicating_first_name = State()
    indicating_last_name = State()
    indicating_surname = State()
    indicating_mobile_num = State()
    indicating_birthday = State()
    indicating_email = State()
    confirm = State()


@router.callback_query(F.data.startswith('yes_create'), StateFilter(None))
async def yes_create(call: CallbackQuery, state: FSMContext):
    if not check.rus_str(f'{call.from_user.first_name}'):
        data = Text('''
Я не смог определить твои имя и фамилию.
Для создания профиля необходимо внести их вручную\n\n''',
                    Bold("Введи имя:"))
        await call.message.edit_text(**data.as_kwargs())
        await state.set_state(CreateProfile.indicating_first_name)
    elif check.rus_str(f'{call.from_user.last_name}'):
        data = Text("Я определил твои имя и фамилию:",
                    BlockQuote("Имя: ", string.capwords(call.from_user.first_name),
                               "\nФамилия: ", string.capwords(call.from_user.last_name)),
                    "Добавить эти данные или ты внесёшь их вручную?\n",
                    Bold("‼️Важно: Добавляй полное имя‼️"))
        await call.message.edit_text(**data.as_kwargs(), reply_markup=kb.creating_profile())
    else:
        data = Text("Я смог определить только твоё имя:",
                    BlockQuote("Имя: ", string.capwords(call.from_user.first_name)),
                    "Сохранить его или ты желаешь внести изменения?\n",
                    Bold("‼️Важно: Добавляй полное имя‼️"))
        await call.message.edit_text(**data.as_kwargs(), reply_markup=kb.creating_profile())
    await call.answer(cache_time=5)


@router.callback_query(F.data.startswith('no_manual'), StateFilter(None))
async def manual_create(call: CallbackQuery, state: FSMContext):
    await call.answer(f'Если что-то сломалось или хочешь отменить, введи /clear или выбери эту команду из меню')
    await call.message.edit_text(f'<b>Введи имя</b>')
    await state.set_state(CreateProfile.indicating_first_name)
    await call.answer(cache_time=5)


@router.callback_query(F.data.startswith('yes_this'), StateFilter(None))
async def create_with_data(call: CallbackQuery, state: FSMContext):
    if not check.rus_str(f'{call.from_user.last_name}'):
        await state.update_data(first_name=string.capwords(call.from_user.first_name))
        await call.message.edit_text(f'''
Указанные данные:<blockquote>
Имя: {string.capwords(call.from_user.first_name)}</blockquote>
<b>Введи фамилию</b>''')
        await state.set_state(CreateProfile.indicating_last_name)
    else:
        await state.update_data(
            first_name=string.capwords(call.from_user.first_name),
            last_name=string.capwords(call.from_user.last_name)
        )
        await call.message.delete()
        await call.message.answer(f'''
        Указанные данные:<blockquote>
        Имя: {string.capwords(call.from_user.first_name)}
        Фамилия: {string.capwords(call.from_user.last_name)}</blockquote>
        Укажи отчество (можно пропустить)''', reply_markup=kb.skip())
        await state.set_state(CreateProfile.indicating_surname)


@router.message(F.text, init.isValid(), CreateProfile.indicating_first_name)
async def first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=string.capwords(message.text))
    student_data = await state.get_data()
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}</blockquote>
<b>Введи фамилию</b>''')
    await state.set_state(CreateProfile.indicating_last_name)


@router.message(F.text, init.isValid(), CreateProfile.indicating_last_name)
async def last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=string.capwords(message.text))
    student_data = await state.get_data()
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}
Фамилия: {student_data['last_name']}</blockquote>
Укажи отчество (можно пропустить)''', reply_markup=kb.skip())
    await state.set_state(CreateProfile.indicating_surname)


@router.message(F.text, init.isValid(), CreateProfile.indicating_surname)
async def surname(message: Message, state: FSMContext):
    if message.text != "Пропустить":
        await state.update_data(surname=string.capwords(message.text))
    else:
        await state.update_data(surname=None)
    student_data = await state.get_data()
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}
Фамилия: {student_data['last_name']}
Отчество: {student_data['surname'] if (student_data['surname'] != None) else 'Не указано'}</blockquote>
Укажи номер телефона или отправь свой контакт (можно пропустить). <u><b>Формат номера: </b></u><i>+79121231234</i>''',
                         reply_markup=kb.req_contact())
    await state.set_state(CreateProfile.indicating_mobile_num)


@router.message(F.contact, CreateProfile.indicating_mobile_num)
async def mobile_num(message: Message, state: FSMContext):
    num = message.contact
    if "+" in num.phone_number:
        await state.update_data(mobile_num=num.phone_number)
    else:
        await state.update_data(mobile_num=("+" + num.phone_number))
    student_data = await state.get_data()
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}
Фамилия: {student_data['last_name']}
Отчество: {student_data['surname'] if (student_data['surname'] != None) else 'Не указано'}
Номер телефона: {student_data['mobile_num'] if (student_data['mobile_num'] != None) else 'Не указано'}</blockquote>
Укажи свою дату рождения (можно пропустить)''', reply_markup=kb.skip())
    await state.set_state(CreateProfile.indicating_birthday)


@router.message(F.text, init.mobileNum(), CreateProfile.indicating_mobile_num)
async def mobile_number(message: Message, state: FSMContext):
    mobile_num: str
    if message.text != "Пропустить":
        await state.update_data(mobile_num=message.text)
    else:
        await state.update_data(mobile_num=None)
    student_data = await state.get_data()
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}
Фамилия: {student_data['last_name']}
Отчество: {student_data['surname'] if (student_data['surname'] != None) else 'Не указано'}
Номер телефона: {student_data['mobile_num'] if (student_data['mobile_num'] != None) else 'Не указано'}</blockquote>
Укажи свою дату рождения (можно пропустить)''', reply_markup=kb.skip())
    await state.set_state(CreateProfile.indicating_birthday)


@router.message(F.text, init.date(), CreateProfile.indicating_birthday)
async def birthday(message: Message, state: FSMContext):
    reply = ""
    if message.text == "Пропустить":
        await state.update_data(birthday=None)
    else:
        normalized = dateFunc.normalize_date_format(message.text)
        await state.update_data(birthday=normalized)
    student_data = await state.get_data()
    if student_data['birthday'] != None:
        date_str = student_data['birthday']
        bd_to_parse = dateFunc.parse_date(date_str)
        reply = f'''{bd_to_parse['day']} {bd_to_parse['month']} {bd_to_parse['year']}'''
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}
Фамилия: {student_data['last_name']}
Отчество: {student_data['surname'] if (student_data['surname'] != None) else 'Не указано'}
Номер телефона: {student_data['mobile_num'] if (student_data['mobile_num'] != None) else 'Не указано'}
Дата рождения: {reply if (student_data['birthday'] != None) else 'Не указано'}</blockquote>
Укажи свой email (можно пропустить)''', reply_markup=kb.skip())
    await state.set_state(CreateProfile.indicating_email)


@router.message(F.text, init.email(), CreateProfile.indicating_email)
async def email(message: Message, state: FSMContext):
    if message.text != "Пропустить":
        await state.update_data(email=message.text.lower())
    else:
        await state.update_data(email=None)
    student_data = await state.get_data()
    reply = ""
    if student_data['birthday'] != None:
        date_str = student_data['birthday']
        bd_to_parse = dateFunc.parse_date(date_str)
        reply = f'''{bd_to_parse['day']} {bd_to_parse['month']} {bd_to_parse['year']}'''
    await message.answer(f'''
Указанные данные:<blockquote>
Имя: {student_data['first_name']}
Фамилия: {student_data['last_name']}
Отчество: {student_data['surname'] if (student_data['surname'] != None) else 'Не указано'}
Номер телефона: {student_data['mobile_num'] if (student_data['mobile_num'] != None) else 'Не указано'}
Дата рождения: {reply if (student_data['birthday'] != None) else 'Не указано'}
Email: {student_data['email'] if (student_data['email'] != None) else 'Не указано'}
</blockquote>
Верны ли эти данные?
''', reply_markup=kb.confirm_data())
    await state.set_state(CreateProfile.confirm)


@router.callback_query(F.data.startswith('yes_confirm'), CreateProfile.confirm)
async def crate_student(call: CallbackQuery, state: FSMContext):
    student_dict = await state.get_data()
    await db.add_student(student_dict, call.from_user.username, str(call.message.chat.id))
    await call.message.answer(text='Данные успешно сохранены', reply_markup=kb.main_kb())
    await state.clear()
    await call.answer(cache_time=5)


@router.callback_query(F.data.startswith('no_confirm'), CreateProfile.confirm)
async def no_confirm(call: CallbackQuery, state: FSMContext):
    text = f'''
Хорошо!
Для доступа к функционалу бота необходимо создать профиль.
Ты можешь сделать это по кнопке "Мой профиль"'''
    await call.answer(cache_time=5)
    await state.clear()
    await call.message.edit_text(f'{text}')
    await call.message.answer(f'Выбери раздел:', reply_markup=kb.main_kb())


@router.message(Command("clear"))
async def clear_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'State очищен', reply_markup=kb.main_kb())


@router.callback_query(F.data.startswith('no_create'))
async def no_create(call: CallbackQuery):
    text = f'''
Хорошо!
Для доступа к функционалу бота необходимо создать профиль.
Ты можешь сделать это по кнопке "Мой профиль"'''
    await call.answer(cache_time=5)
    await call.message.edit_text(f'{text}')
    await call.message.answer(f'Выбери раздел:', reply_markup=kb.main_kb())
