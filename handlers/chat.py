import requests
from aiogram import types, Dispatcher
from bot.config import open_toxic_token
from bot.create_bot import dp, bot

import json
from bot.config import open_toxic_token

# @dp.message_handler(content_types=["text"])
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
            #counter += 1

    except Exception as e:
        await message.reply(f"Ошибка: {e}")


def register_handlers_chat(dp: Dispatcher):
    dp.register_message_handler(on_message, content_types=['text'])