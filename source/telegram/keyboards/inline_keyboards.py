from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💻📱Мои устройства', callback_data='Мои устройства')],
    [InlineKeyboardButton(text='🗂Помощь', callback_data='Помощь'), InlineKeyboardButton(text='💳Баланс', callback_data='Баланс')],
    [InlineKeyboardButton(text='💰Реферальная система', callback_data='Реферальная система'),],
    [ InlineKeyboardButton(text='🏅 Пробный период', callback_data='Пробный период')]
])