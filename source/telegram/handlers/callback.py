import time

from aiogram import types
from source.telegram.keyboards.inline_keyboards import device
from source.telegram.config import MESSAGE


async def callback_def(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if callback_query.data == 'Мои устройства':

        await callback_query.message.answer(MESSAGE['device_1'], reply_markup=device(2312))

    if callback_query.data == 'Баланс':
        await callback_query.message.answer('Ваш баланс равен: ')