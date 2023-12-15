from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, reply_keyboard_remove, CallbackQuery
from lexicon.lexicon_ru import MESSAGE_TEXT
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from services.googlesheets import append_client, update_birthday, update_phone, update_zapros, update_photo
from keyboards.keyboard import *
from keyboards.calendar import *
from config_data.config import Config, load_config
from aiogram import Bot

from datetime import date

from aiogram.types import CallbackQuery



router = Router()


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

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext) -> None:
    await message.answer(text=MESSAGE_TEXT['/start'])

    file_id = 'AgACAgIAAxkBAAID62V7PJxkpl-S7yifd70ICjD_eWDOAALG2jEb2xzZSzBke6AVjDYnAQADAgADeQADMwQ'
    file_unique_id = 'AQADxtoxG9sc2Ut-'
    await message.answer_photo(file_id, caption=MESSAGE_TEXT['presentation'])

    await message.answer(text=MESSAGE_TEXT['get_name'])
    await state.set_state(Form.name)

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=MESSAGE_TEXT['/help'])


# Отлавливаем Имя пользователя
@router.message(StateFilter(Form.name), F.text.isalpha())
async def process_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(text=f'Привет, {message.text}')
    await state.update_data(name=message.text)
    append_client(message.chat.id, message.text)
    await state.set_state(Form.birthday)
    keyboard = get_calendar_keyboard()
    await message.answer(text=MESSAGE_TEXT['get_birthday'])



# Отлавливаем ошибку ввода имени пользователя
@router.message(StateFilter(Form.name))
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(text='То что вы отправили не похоже на имя')


# Отлавливаем дату рождения пользователя
@router.message(Form.birthday)
async def process_birthday(message: Message, state: FSMContext) -> None:
    update_birthday(message)
    await state.update_data(birthday=message.text)
    await state.set_state(Form.phone)
    keyboard = get_contact()
    await message.answer(text=MESSAGE_TEXT['get_phone'], reply_markup=keyboard)


# Отлавливаем телефон пользователя
# @router.message(content_types='contact')
@router.message(StateFilter(Form.phone))
async def process_phone(message: Message, state: FSMContext) -> None:
    update_phone(message)
    if message.contact != None:
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
    else:
        phone = message.text
        await state.update_data(phone=phone)
    await state.set_state(Form.zapros)
    markup = types.ReplyKeyboardRemove()
    await message.answer(text=MESSAGE_TEXT['zapros'], reply_markup=markup)


# Отлавливаем запрос пользователя
@router.message(Form.zapros)
async def process_zapros(message: Message, state: FSMContext) -> None:
    update_zapros(message)
    await state.update_data(zapros=message.text)
    keyboard = keyboard_begin()
    await message.answer(text=MESSAGE_TEXT['begin'], reply_markup=keyboard)


# НАЧАТЬ
@router.callback_query(F.data == 'beg')
async def process_buttons_press(callback: CallbackQuery):
    await callback.message.answer(text=MESSAGE_TEXT['sonastroika'])
    keyboard = keyboard_sonastroika()
    await callback.answer()
    await callback.message.answer(text=MESSAGE_TEXT['sonostroika2'], reply_markup=keyboard)


@router.callback_query(F.data == 'sonastroika')
async def process_buttons_press(callback: CallbackQuery):
    file_id = 'BAACAgIAAxkBAAICFWV4ue48KM4t4EK91cfU2IQh4x0HAAIEQgAC0z7IS7_e9PPsWVogMwQ'
    file_unique_id = 'AgADBEIAAtM-yEs'
    keyboard = keyboard_sonastroika1()
    await callback.message.answer_video(file_id, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == 'pass')
async def process_stage1(callback: CallbackQuery):
    keyboard = keyboard_stage1()
    await callback.answer()
    file_id = 'AgACAgIAAxkBAAICXGV4vpgZ2qktpv-sPd-MUVVaCMPMAAJx0jEb0z7IS9_r8FYtrYQJAQADAgADeQADMwQ'
    await callback.message.answer_photo(photo=file_id, caption=MESSAGE_TEXT['stage1'], reply_markup=keyboard)

# @router.callback_query(F.data=='photo_stage1')
# async def process_stage1(callback: CallbackQuery):
#     file_id = 'AgACAgIAAxkBAAICXGV4vpgZ2qktpv-sPd-MUVVaCMPMAAJx0jEb0z7IS9_r8FYtrYQJAQADAgADeQADMwQ'
#     file_unique_id = 'AQADcdIxG9M-yEt-'
#     await callback.message.answer_photo(file_id)


@router.callback_query(F.data=='photo_stage3')
async def process_buttons_press(callback: CallbackQuery):
    file_id = 'AgACAgIAAxkBAAICYGV4v35xZmB41ClGLpesMojJdo_UAAJ50jEb0z7ISwuH-jQDDYlvAQADAgADeQADMwQ'
    file_unique_id = 'AQADedIxG9M-yEt-'
    await callback.message.answer_photo(file_id)


# @router.callback_query(F.data=='photo_stage2')
# async def process_buttons_press(callback: CallbackQuery):
#     file_id = 'AgACAgIAAxkBAAICXmV4v0-b1V9i61zYSAABidS3YaUmMAACeNIxG9M-yEu_oysMuEMLPwEAAwIAA3kAAzME'
#     file_unique_id = 'AQADeNIxG9M-yEt-'
#     await callback.message.answer_photo(file_id)

@router.callback_query(F.data=='done_stage1')
async def process_buttons_press(callback: CallbackQuery):
    keyboard = keyboard_stage2()
    file_id = 'AgACAgIAAxkBAAICYGV4v35xZmB41ClGLpesMojJdo_UAAJ50jEb0z7ISwuH-jQDDYlvAQADAgADeQADMwQ'
    await callback.answer()
    await callback.message.answer_photo(photo=file_id, caption=MESSAGE_TEXT['stage2'])
    await callback.message.answer(text=MESSAGE_TEXT['stage2_1'])
    await callback.message.answer(text=MESSAGE_TEXT['stage2_2'], reply_markup=keyboard)

@router.callback_query(F.data=='done_stage2')
async def process_buttons_press(callback: CallbackQuery):
    keyboard = keyboard_stage3()
    await callback.answer()
    file_id = 'AgACAgIAAxkBAAICXmV4v0-b1V9i61zYSAABidS3YaUmMAACeNIxG9M-yEu_oysMuEMLPwEAAwIAA3kAAzME'
    await callback.message.answer_photo(photo=file_id, caption=MESSAGE_TEXT['stage3'], reply_markup=keyboard)


@router.callback_query(F.data=='done_stage3')
async def process_stage3(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.photo)
    await callback.answer()
    await callback.message.answer(text=MESSAGE_TEXT['get_photo'])



@router.message(F.photo, Form.photo)
async def get_photo(message: Message, state: FSMContext, bot: Bot):
    print('get_photo')
    file_id = message.photo[-1].file_id
    update_photo(message, file_id)
    user_dict[message.chat.id] = await state.get_data()
    config: Config = load_config()

    await bot.send_photo(chat_id=843554518, photo=file_id, caption=f'ИМЯ: {user_dict[message.chat.id]["name"]}\n'
                                             f'ДАТА РОЖДЕНИЯ: {user_dict[message.chat.id]["birthday"]}\n'
                                             f'НОМЕР ТЕЛЕФОНА: {user_dict[message.chat.id]["phone"]}\n'
                                             f'ЗАПРОС: {user_dict[message.chat.id]["zapros"]}')
    await message.answer(text=MESSAGE_TEXT['text1'])
    keyboard = keyboard_finish()
    await message.answer(text=MESSAGE_TEXT['finish'], reply_markup=keyboard)
    # url = f'https://api.telegram.org/file/bot{config.tg_bot.token}/{file.file_path}'

@router.message(Form.photo)
async def get_photo(message: Message):
    await message.answer(text='Это не похоже на фото! Пришли мне фото')

@router.callback_query(F.data=='chekin')
async def process_stage3(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.answer()
    await bot.send_message(chat_id=843554518, text=f'Пользователь {callback.message.from_user.username} записался на полный разбор!')

    await callback.message.answer(text=MESSAGE_TEXT['text2'])
    await callback.message.answer(text=MESSAGE_TEXT['text3'])