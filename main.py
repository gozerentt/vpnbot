import asyncio
import logging
from aiogram import Bot, Dispatcher


from source.telegram.config import TOKEN_TG
from source.telegram.handlers.router_main import router

bot = Bot(token=TOKEN_TG)
dp = Dispatcher()


async def main():

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
