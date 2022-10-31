
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.create_bot import dp, bot
from bot.keyboards import admin_keyboard
from bot.data_base import sqlite_db


ID = None

# @dp.message_handler(commands='info')
async def load_info(message: types.Message):
    if message.from_user.id == ID:
        await sqlite_db.sql_read(message)

class FSMAdmin(StatesGroup):
    toxic_words = State()


#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что требуется сделать?', reply_markup=admin_keyboard.button_case_admin)
    await message.delete()

# @dp.message_handler(commands='Добавить слово', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.toxic_words.set()
        await message.reply('Какое слово добавить в запрещенные?')

# @dp.message_handler(state=FSMAdmin.toxic_words)
async def load_word(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['toxic_words'] = message.text
        await message.reply("Слово добавлено")

        await sqlite_db.sql_add_command(state)
        await state.finish()

# Выход из состояний
# @dp.message_handler(state="*", commands = 'Отмена')
# @dp.message_handler(Text(equals='Отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')

def register_handlers_admin(dp: Dispatcher):
  dp.register_message_handler(load_info, commands=['info'])
  dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
  dp.register_message_handler(cm_start, commands=['add'], state=None)
  dp.register_message_handler(load_word, state=FSMAdmin.toxic_words)
  dp.register_message_handler(cancel_handler, state="*", commands=['Cancel'])
  dp.register_message_handler(cancel_handler, Text(equals=['Cancel'], ignore_case=True), state="*")
