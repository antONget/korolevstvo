from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicon.lexicon_ru import MESSAGE_TEXT

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(Command(commands=['admin']))
async def send_answer(message: Message):
    await message.answer(text=MESSAGE_TEXT['/admin'])