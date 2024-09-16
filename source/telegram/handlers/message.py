from aiogram import Router, types, Bot
from aiogram.types import Message

router = Router()


async def message_def(message: Message):
    await message.reply('fdfd')