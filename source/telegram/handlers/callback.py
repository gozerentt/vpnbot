import time

from aiogram import Router, types, Bot


async def callback_def(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    if callback_query.data == 'Мои устройства':

        await callback_query.message.answer('3232')