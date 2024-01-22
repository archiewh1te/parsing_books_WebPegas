from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import load_config

config = load_config('.env')  # Load the configuration from .env file

bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)

storage=MemoryStorage()

dp = Dispatcher(bot, storage=storage)


__all__ = ['bot', 'storage', 'dp']