from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from  config import tg_token_bot

storage = MemoryStorage()

bot = Bot(token=tg_token_bot)
dp = Dispatcher(bot, storage=storage)

counter = 0
