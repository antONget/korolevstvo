from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from lexicon.lexicon_ru import MESSAGE_TEXT
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from services.googlesheets import append_client, append_start, update_birthday, update_phone, update_zapros, update_photo
from keyboards.keyboard import *
from aiogram import Bot
from aiogram.types import CallbackQuery
from datetime import datetime


router = Router()
admin_id = 713697088

# состояния бота
class Form(StatesGroup):
    name = State()
    phone = State()
    birthday = State()
    question = State()
    zapros = State()
    photo = State()


# Создаем "базу данных" пользователей
user_dict = {}


# Этот хэндлер срабатывает на команду /start, States -> name
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext) -> None:
    now = datetime.now()
    today = now.strftime("%d/%m/%Y")
    append_start(message.chat.id, today)
    file_id_1 = "AgACAgIAAxkBAAOiZX2YRiLAYNbAjVZQyiogQZ0UsN4AAlvPMRuERPBLD0MTby2BjhgBAAMCAAN5AAMzBA"
    await message.answer_photo(file_id_1, caption=MESSAGE_TEXT['presentation'])
    await message.answer(text=MESSAGE_TEXT['get_name'])
    await state.set_state(Form.name)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=MESSAGE_TEXT['/help'])


# Отлавливаем Имя пользователя состоящее только из букв и переводит в сотояние ввода даты рождения, States -> birthday
@router.message(StateFilter(Form.name), F.text.isalpha())
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(text=f'Привет, {message.text}')
    await state.update_data(name=message.text)
    append_client(message.chat.id, message.text)
    await state.set_state(Form.birthday)
    await message.answer(text=MESSAGE_TEXT['get_birthday'])


# Отлавливаем ошибку ввода имени пользователя, если оно состоит не только из букв
@router.message(StateFilter(Form.name))
async def process_name(message: Message) -> None:
    await message.answer(text='То что вы отправили не похоже на имя')


# Отлавливаем дату рождения пользователя, , States -> phone
@router.message(Form.birthday)
async def process_birthday(message: Message, state: FSMContext) -> None:
    update_birthday(message)
    await state.update_data(birthday=message.text)
    await state.set_state(Form.phone)
    keyboard = get_contact()
    await message.answer(text=MESSAGE_TEXT['get_phone'], reply_markup=keyboard)


# Отлавливаем телефон пользователя, States -> zapros
@router.message(StateFilter(Form.phone))
async def process_phone(message: Message, state: FSMContext) -> None:
    update_phone(message)
    if message.contact is not None:
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
    else:
        phone = message.text
        await state.update_data(phone=phone)
    await state.set_state(Form.zapros)
    markup = types.ReplyKeyboardRemove()
    await message.answer(text=MESSAGE_TEXT['zapros'], reply_markup=markup)


# Отлавливаем запрос пользователя на игру
@router.message(Form.zapros)
async def process_zapros(message: Message, state: FSMContext) -> None:
    update_zapros(message)
    await state.update_data(zapros=message.text)
    keyboard = keyboard_begin()
    await message.answer(text=MESSAGE_TEXT['begin'], reply_markup=keyboard)
    await state.set_state(default_state)


# нажата кнопка "НАЧАТЬ"
@router.callback_query(F.data == 'beg')
async def process_buttons_press(callback: CallbackQuery):
    await callback.message.answer(text=MESSAGE_TEXT['sonastroika'])
    keyboard = keyboard_sonastroika()
    await callback.message.answer(text=MESSAGE_TEXT['sonostroika2'], reply_markup=keyboard)
    await callback.answer()


# нажата кнопка "Сонастройка"
@router.callback_query(F.data == 'sonastroika')
async def process_buttons_press(callback: CallbackQuery):
    file_id_2 = 'BAACAgIAAxkBAAMaZX2C7Tm-KMelRVVgJcptI8mqqjAAArBAAAKERPBLNmnlXtsLv3AzBA'
    keyboard = keyboard_sonastroika1()
    await callback.message.answer_video(file_id_2, reply_markup=keyboard)
    await callback.answer()


# нажата кнопка "Дальше" -> первый этап игры
@router.callback_query(F.data == 'pass')
async def process_stage1(callback: CallbackQuery):
    keyboard = keyboard_stage1()
    await callback.answer()
    file_id_stage1 = 'AgACAgIAAxkBAAMcZX2DMP9OUsfqGLN6xzPeQwblEloAAr_OMRuERPBL54rWglK0zp8BAAMCAAN5AAMzBA'
    await callback.message.answer_photo(photo=file_id_stage1, caption=MESSAGE_TEXT['stage1'], reply_markup=keyboard)


# нажата кнопка "Готово" -> воторой этап игры
@router.callback_query(F.data == 'done_stage1')
async def process_buttons_press(callback: CallbackQuery):
    keyboard = keyboard_stage2()
    file_id_stage2 = 'AgACAgIAAxkBAAMeZX2DcEaJsqlO6ndVmPA0Muj9_dUAAsHOMRuERPBLHZ6pl9mQdzsBAAMCAAN5AAMzBA'
    await callback.message.answer_photo(photo=file_id_stage2, caption=MESSAGE_TEXT['stage2'])
    await callback.message.answer(text=MESSAGE_TEXT['stage2_1'])
    await callback.message.answer(text=MESSAGE_TEXT['stage2_2'], reply_markup=keyboard)
    await callback.answer()


# нажата кнопка "Готово" -> третий этап игры
@router.callback_query(F.data == 'done_stage2')
async def process_buttons_press(callback: CallbackQuery):
    keyboard = keyboard_stage3()
    file_id_stage3 = 'AgACAgIAAxkBAAMgZX2DqTlSe1ooh4QKK2B8aJCyCy4AAsLOMRuERPBLCjF3gGFospwBAAMCAAN5AAMzBA'
    await callback.message.answer_photo(photo=file_id_stage3, caption=MESSAGE_TEXT['stage3'], reply_markup=keyboard)
    await callback.answer()


# нажата кнопка "Готово" -> запрос отправки фото, State -> photo
@router.callback_query(F.data == 'done_stage3')
async def process_stage3(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.photo)
    await callback.answer()
    await callback.message.answer(text=MESSAGE_TEXT['get_photo'])


# отлавливаем фото
@router.message(F.photo, Form.photo)
async def get_photo(message: Message, state: FSMContext, bot: Bot):
    file_id = message.photo[-1].file_id
    update_photo(message, file_id)
    user_dict[message.chat.id] = await state.get_data()
    await bot.send_photo(chat_id=admin_id,
                         photo=file_id,
                         caption=f'ИМЯ: {user_dict[message.chat.id]["name"]}\n'
                                 f'ДАТА РОЖДЕНИЯ: {user_dict[message.chat.id]["birthday"]}\n'
                                 f'НОМЕР ТЕЛЕФОНА: {user_dict[message.chat.id]["phone"]}\n'
                                 f'ЗАПРОС: {user_dict[message.chat.id]["zapros"]}')
    await message.answer(text=MESSAGE_TEXT['text1'])
    keyboard = keyboard_finish()
    await message.answer(text=MESSAGE_TEXT['finish'], reply_markup=keyboard)
    await state.clear()


# если отправляют не фото
@router.message(Form.photo)
async def get_photo(message: Message):
    await message.answer(text='Это не похоже на фото! Пришли мне фото')


# нажата кнопка "Записаться"
@router.callback_query(F.data == 'chekin')
async def process_stage3(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.message.chat.username is not None:
        await bot.send_message(chat_id=admin_id, text=f'Пользователь <a href="https://t.me/{callback.message.chat.username}">'
                                                    f'{callback.message.chat.username}</a>'
                                                    f' записался на полный разбор!')
    else:
        await bot.send_message(chat_id=admin_id, text=f'Пользователь c ID={callback.message.chat.id}'
                                                      f' записался на полный разбор!')
    await callback.message.answer(text=MESSAGE_TEXT['text2'])
    await callback.message.answer(text=MESSAGE_TEXT['text3'])
    await callback.answer()
