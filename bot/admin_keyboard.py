from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/Добавить слово')
button_info = KeyboardButton('/Информация')
button_delete = KeyboardButton('/Удалить слово')


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
            .add(button_info).add(button_delete)
