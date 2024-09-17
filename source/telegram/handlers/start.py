from aiogram.types import Message
from contextlib import suppress

from source.telegram.config import MESSAGE
from source.telegram.keyboards.inline_keyboards import start_kb


users = []
message_ids = []
async def start_def(message: Message):
    global message_id

    if message.from_user.id not in users:
        await message.delete()
        message_id =  message.answer(f'{message.from_user.first_name}{MESSAGE["firs          t_start"]}', reply_markup=start_kb)
        users.append(message.from_user.id)

    else:
        await message.delete()
        await message.answer(f'{message.from_user.first_name}{MESSAGE["first_start"]}', reply_markup=start_kb)