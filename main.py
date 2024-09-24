import os
import zipfile
import asyncio
from datetime import datetime, timedelta

import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

from dynamic_and_static_data.dynamic_and_static_data import save_local_botlang
from filters.chat_type_filter import DuplicatesMiddleware
from handlers.admin_handlers import admin_router
from handlers.users_handlers import user_router

#API_TOKEN = '7388733347:AAFbxGzFkdwNRNLxieb7Z9fZuk15HB2Fbks' #Prod
#API_TOKEN = '7409271656:AAF8jvGPlm8xFJfA2_OuzWK3SpO3MwFATDE' #Dodantest
API_TOKEN = '7195566516:AAFeE9-hxd01oAi2Pf92mGQCvw2oOERkPoQ'  #testpict2

bot = Bot(API_TOKEN)
dp = Dispatcher()
dp.callback_query.middleware(DuplicatesMiddleware())

dp.include_router(admin_router)
dp.include_router(user_router)





async def save_global_data():
    while True:
        now = datetime.now()
        scheduled_time = now.replace(hour=2, minute=0, second=0, microsecond=0)
        if now > scheduled_time:
            scheduled_time += timedelta(days=1)
        time_until_execution = (scheduled_time - now).total_seconds()
        await asyncio.sleep(time_until_execution)
        await save_local_botlang()


async def main():
    save_global = save_global_data()
    asyncio.create_task(save_global)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
