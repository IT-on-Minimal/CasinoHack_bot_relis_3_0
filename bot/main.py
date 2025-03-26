import sys
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.dp import init_db
from handlers import start as start_router
from handlers import admin_handlers
from handlers import user_handlers


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    init_db()

    dp.include_router(start_router.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
