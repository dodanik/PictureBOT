import os
import zipfile
import asyncio
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

from handlers.admin_handlers import admin_router
from handlers.users_handlers import user_router

API_TOKEN = '7409271656:AAF8jvGPlm8xFJfA2_OuzWK3SpO3MwFATDE'
bot = Bot(API_TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_router)









async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
