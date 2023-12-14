from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram import types


def get_contact():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   keyboard=[[KeyboardButton(text='Отправить номер телефона',
                                                             request_contact=True)]])
    return keyboard

def keyboard_begin():
    # Создаем объекты инлайн-кнопок
    button = InlineKeyboardButton(
        text='НАЧАТЬ',
        callback_data='beg'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
    print("keyboard_begin")
    return keyboard


def keyboard_sonastroika():
    # Создаем объекты инлайн-кнопок
    button_s = InlineKeyboardButton(
        text='Сонастройка',
        callback_data='sonastroika'
    )
    button_p = InlineKeyboardButton(
        text='Дальше',
        callback_data='pass'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_s, button_p]]
    )
    return keyboard


def keyboard_stage1():
    # Создаем объекты инлайн-кнопок
    button_photo = InlineKeyboardButton(
        text='Фото-образец',
        callback_data='photo_stage1'
    )
    button_done = InlineKeyboardButton(
        text='Готово',
        callback_data='done_stage1'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_photo, button_done]]
    )
    return keyboard


def keyboard_stage2():
    # Создаем объекты инлайн-кнопок
    button_photo = InlineKeyboardButton(
        text='Фото-образец',
        callback_data='photo_stage2'
    )
    button_done = InlineKeyboardButton(
        text='Готово',
        callback_data='done_stage2'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_photo, button_done]]
    )
    return keyboard


def keyboard_stage3():
    # Создаем объекты инлайн-кнопок
    button_photo = InlineKeyboardButton(
        text='Фото-образец',
        callback_data='photo_stage3'
    )
    button_done = InlineKeyboardButton(
        text='Готово',
        callback_data='done_stage3'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_photo, button_done]]
    )
    return keyboard


def keyboard_finish():
    # Создаем объекты инлайн-кнопок
    button = InlineKeyboardButton(
        text='ЗАПИСАТЬСЯ',
        callback_data='chekin'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
    print("keyboard_begin")
    return keyboard