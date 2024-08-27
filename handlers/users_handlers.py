import re
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from dynamic_and_static_data.dynamic_and_static_data import get_botlang, save_botlang
from filters.chat_type_filter import ChatTypesFilter
from aiogram import types, F

from keyboards.user.create_kb_promoactions import create_kb_promoactions
from keyboards.user.general_menu_kb import create_general_menu
from keyboards.user.kb_bot_lang import get_language_keyboard
from keyboards.user.kb_download_select_lang import create_download_lang_menu
from keyboards.user.settings_user_menu import create_settings_menu

user_router = Router()
user_router.message.filter(ChatTypesFilter(['private']))






class Download(StatesGroup):
    lang = State()
    name_baner = State()
    promocode = State()








@user_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("You have entered the Name banner bot, please select a language",
                         reply_markup=await get_language_keyboard())


@user_router.callback_query(lambda c: c.data.startswith('lang_'))
async def process_callback(callback_query: types.CallbackQuery):
    # Извлекаем данные из callback_data
    language_code = callback_query.data
    botlang = await get_botlang()

    # Определяем ответ в зависимости от языка
    if language_code == 'lang_ru':
        botlang[callback_query.message.chat.id] = 'ru'
        response_text = "Вы выбрали русский язык."
    elif language_code == 'lang_en':
        botlang[callback_query.message.chat.id] = 'en'
        response_text = "You selected English."
    elif language_code == 'lang_uz':
        botlang[callback_query.message.chat.id] = 'uz'
        response_text = "Siz o'zbek tilini tanladingiz."
    else:
        response_text = "Язык не выбран."

    # Отправляем ответ пользователю
    await callback_query.message.answer(response_text, reply_markup=await create_general_menu(botlang[callback_query.message.chat.id]))

    # Удаляем инлайн-клавиатуру, если необходимо
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await save_botlang(botlang)







@user_router.message((F.text == "Settings") | (F.text == "Настройки") | (F.text == "Sozlamalar"))
async def settings(message: types.Message, state: FSMContext):
    botlang = await get_botlang()
    await message.answer("Press the corresponding key to change",
                         reply_markup=await create_settings_menu(botlang[message.chat.id]))


@user_router.callback_query(lambda c: c.data.startswith('setting_lang'))
async def settings_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=await get_language_keyboard())




@user_router.message((F.text == "Download") | (F.text == "Скачать") | (F.text == "Yuklab olish"))
async def download(message: types.Message, state: FSMContext):
    await state.clear()
    botlang = await get_botlang()
    await message.answer("Select language to download",
                         reply_markup=await create_download_lang_menu())



@user_router.callback_query(lambda c: c.data.startswith('download_lang_'))
async def download_lang_callback(callback_query: types.CallbackQuery):
    botlang = await get_botlang()
    lang_selected = callback_query.data.split('_')[-1] or "en"

    await callback_query.message.answer("Select the type of banners you would like to download. Next, you will be able to enter promocode",
                                        reply_markup=await create_kb_promoactions(lang_selected))





@user_router.callback_query(lambda c: c.data.startswith('name_baner_'))
async def download_name_baner_callback(callback_query: types.CallbackQuery, state: FSMContext):
    botlang = await get_botlang()
    name_baner = callback_query.data.split('name_baner_', 1)[-1]
    await callback_query.message.answer("Enter the promo code text:")


@user_router.message(Download.promocode, F.text)
async def download_promocode(message: types.Message, state: FSMContext):
    botlang = await get_botlang()
    if re.match(r'^[A-Za-z0-9]{1,20}$', message.text):
        await state.update_data(promocode=message.text)
        #функция генерации данных для отправки афилиату
        data = await state.get_data()
        await message.answer(f'{data["lang"]}    {data["name_baner"]}    {data["promocode"]}', reply_markup=await create_general_menu(botlang[message.chat.id]))
        await state.clear()
    else:
        await message.answer("Please enter the correct promotional code:")
        await state.set_state(Download.promocode)
