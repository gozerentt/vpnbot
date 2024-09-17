from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup

user_tokens = ['token1234', 'token4321', 'token2341', 'token2134']

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💻📱Мои устройства', callback_data='Мои устройства')],
    [InlineKeyboardButton(text='🗂Помощь', callback_data='Помощь'), InlineKeyboardButton(text='💳Баланс', callback_data='Баланс')],
    [InlineKeyboardButton(text='💰Реферальная система', callback_data='Реферальная система'),],
    [ InlineKeyboardButton(text='🏅 Пробный период', callback_data='Пробный период')]
])

def device(user_id):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for token in user_tokens:
        button = InlineKeyboardButton(text=f'🗝{token}', callback_data=token)
        keyboard.inline_keyboard.append([button])

    add_device = InlineKeyboardButton(text='💾Добавить устр.', callback_data='Добавить устр.')
    del_device = InlineKeyboardButton(text='🗑Удалить устр.', callback_data='Удалить устр.')
    start = InlineKeyboardButton(text='🏠Главное меню', callback_data='Главное меню  ')
    help_button = InlineKeyboardButton(text='📑Помощь', callback_data='Помощь')

    keyboard.inline_keyboard.append([add_device, del_device])
    keyboard.inline_keyboard.append([start, help_button])

    return keyboard