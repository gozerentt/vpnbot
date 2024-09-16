from aiogram.types import Message

from source.telegram.config import MESSAGE
from source.telegram.keyboards.inline_keyboards import start_kb



async def start_def(message: Message):
    await message.delete()
    await message.answer(f'{message.from_user.first_name}{MESSAGE["start_message"]}', reply_markup=start_kb)