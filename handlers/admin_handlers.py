from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicon.lexicon_ru import MESSAGE_TEXT
from config_data.config import Config, load_config


router = Router()
config: Config = load_config()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(lambda message: str(message.from_user.id) in config.tg_bot.admin_ids, Command(commands=['admin']))
async def send_admin(message: Message) -> None:
    await message.answer(text=MESSAGE_TEXT['/admin'])
