import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
# from aiogram.dispatcher.filters.state import StatesGroup

from bot.config import tg_bot_token, open_toxic_token

#bot = telebot.TeleBot('5663598777:AAFFwbcgJ4mrIVALO940WfGingesF_BcqNs')

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("Привет, пришли сообщение на проверку")



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
            # await message.reply(f"Токсичное сообщение пользователя @{message['from']['username']}: {message.text}\n")
            await message.delete()

    except Exception as e:
        await message.reply(f"Ошибка: {e}")



if __name__ == '__main__':
    # dp.register_message_handler(on_message)
    executor.start_polling(dp, skip_updates=False)
