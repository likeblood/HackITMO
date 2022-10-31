from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/add')
button_info = KeyboardButton('/info')
button_delete = KeyboardButton('/delete')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
            .add(button_info).add(button_delete)