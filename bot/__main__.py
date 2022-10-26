import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from bot import admin
from config import tg_bot_token, open_toxic_token

import middlewares
from misc.throttling import rate_limit
from db import sqlite_db

# GLOBALS
storage = MemoryStorage()
counter = 0

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=storage)


async def on_startup():
    print('Бот включен')
    middlewares.setup(dp)
    sqlite_db.sql_start()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("Привет, пришли сообщение на проверку")

@rate_limit(limit=10, key=["text"])
@dp.message_handler(content_types=["text"])
async def on_message(message: types.Message):
    try:
        print(message.text)
        r = requests.post(
            f"{open_toxic_token}/predict",
            json={
                "event_type": "toxic_or_not",
                "comment": message.text,
            }
        )
        data = r.json()
        print(data)
        toxic = data["body"]["answer"]

        if toxic == 'toxic' and data["body"]["probability"] > 0.51:
            await message.reply(f"Токсичное сообщение пользователя @{message['from']['username']}: {message.text}\n")
            await message.delete()
            bot.__main__.counter += 1

    except Exception as e:
        await message.reply(f"Ошибка: {e}")


admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
