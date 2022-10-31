from aiogram.utils import executor
from create_bot import dp

from bot.handlers import chat, admin
from bot.data_base import sqlite_db


async def on_startup(_):
    print('Bot is online!')
    sqlite_db.sql_start()

chat.register_handlers_chat(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=False, on_startup=on_startup)