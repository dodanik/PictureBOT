from collections import deque

import ujson as ujson
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.filters import Filter
from aiogram import Bot, types, BaseMiddleware

with open("json_data_file/admin_list.json", "r") as file:
    admins = ujson.load(file)

my_admins_list: list[int] = admins

processed_updates = deque(maxlen=100)

async def my_admins_list_add(id):
    global my_admins_list
    my_admins_list.append(id)
    await save_my_admins_list()


async def my_admins_list_remove(id):
    global my_admins_list
    if id in my_admins_list:
        my_admins_list.remove(id)
        await save_my_admins_list()
        return True
    else:
        return False


async def get_my_admins_list():
    global my_admins_list
    return my_admins_list


async def save_my_admins_list():
    global my_admins_list
    with open("json_data_file/admin_list.json", "w") as json_file:
        ujson.dump(my_admins_list, json_file)


class ChatTypesFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        global my_admins_list
        return message.from_user.id in my_admins_list


class DuplicatesMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, handler, event: types.CallbackQuery, data: dict):
        callback_query_id = event.id  # Используем id колбек-запроса

        if callback_query_id in processed_updates:
            print(f"Duplicate callback query detected: {callback_query_id}")
            raise CancelHandler()  # Отменяем обработку, если дубликат

        # Если нет, добавляем его в список обработанных
        processed_updates.append(callback_query_id)
        # Продолжаем обработку колбек-запроса
        return await handler(event, data)
