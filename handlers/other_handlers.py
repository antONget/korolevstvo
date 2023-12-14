from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import MESSAGE_TEXT

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    print(message)
    await message.answer(text=MESSAGE_TEXT['other_answer'])
