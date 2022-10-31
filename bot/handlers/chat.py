
import re
import requests
from aiogram import types, Dispatcher

from ..config import open_toxic_token
from ..misc.throttling import rate_limit
from ..config import open_toxic_token
from ..data_base.sqlite_db import sql_read_stop_words


def clear_text(string):
    new_string = re.sub('[^а-яА-Я]', ' ', string)
    return re.sub('\s+',' ', new_string)


@rate_limit(limit=10, key=["text"])
# @dp.message_handler(content_types=["text"])
async def on_message(message: types.Message):
    try:
        sw = sql_read_stop_words()
        for word in clear_text(message.text).split():
            if word in sw:
                await message.delete()
                bot.create_bot.counter += 1

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
            bot.create_bot.counter += 1

    except Exception as e:
        await message.reply(f"Ошибка: {e}")


def register_handlers_chat(dp: Dispatcher):
    dp.register_message_handler(on_message, content_types=["text"])

