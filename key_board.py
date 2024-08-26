from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Записать событие')],
    [KeyboardButton(text='Просмотреть события')],
    [KeyboardButton(text='Удалить событие')]
], resize_keyboard=True)
