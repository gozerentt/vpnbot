from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from source.telegram.handlers.message import message_def
from source.telegram.handlers.callback import callback_def
from source.telegram.handlers.start import start_def

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):

    await start_def(message)


@router.callback_query()
async def process_auto_class(callback_query: types.CallbackQuery):
    await callback_def(callback_query)


@router.message(lambda message: types.message)
async def message(message: Message):
    await message_def(message)


