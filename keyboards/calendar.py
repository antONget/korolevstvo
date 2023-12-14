from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
import datetime


def get_calendar_keyboard(year=None, month=None) -> InlineKeyboardMarkup:
    """
    Вывод клаиватуры с календарём для выбора даты
    :return: Клавиатура календаря
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    button = []
    button.append(InlineKeyboardButton(text=str(month),
                                 callback_data=";".join(['ignore', str(0), str(month), str(year)])))
    # keyboard.append(row1)
    row2 = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        button.append(InlineKeyboardButton(text=day,
                                         callback_data=";".join(['ignore', str(day), str(month), str(year)])))
    # keyboard.append(row2)

    my_calendar = calendar.monthcalendar(year, month)
    kb_builder = InlineKeyboardBuilder()
    row3 = []
    for week in my_calendar:
        for day in week:
            if day == 0:
                button.append(InlineKeyboardButton(text=" ",
                                                     callback_data=";".join(
                                                         ['ignore', str(day), str(month), str(year)])))
            else:
                button.append(InlineKeyboardButton(text=str(day),
                                                     callback_data=";".join(['day', str(day), str(month), str(year)])))
    print(len(row3))

    button.append(InlineKeyboardButton(text="<",
                                 callback_data=";".join(['prev_month', str(1), str(month), str(year)])))
    button.append(InlineKeyboardButton(text=" ",
                                 callback_data=";".join(['ignore', str(0), str(month), str(year)])))
    button.append(InlineKeyboardButton(text=">",
                                 callback_data=";".join(['next_month', str(1), str(month), str(year)])))
    # keyboard.append(row4)
    # Создаем объект инлайн-клавиатуры
    kb_builder.row(*button, width=8)

    return kb_builder.as_markup()