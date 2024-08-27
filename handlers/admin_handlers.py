import asyncio
import os
import re
import zipfile
import shutil
from io import BytesIO

from aiogram import Router
from aiogram import Bot, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputFile, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from drawing_function.drawing_function import process_images_and_add_text
from dynamic_and_static_data.dynamic_and_static_data import get_botlang, save_botlang
from filters.chat_type_filter import ChatTypesFilter, IsAdmin
from keyboards.admin.admin_add_stock_menu import admin_add_stock_menu
from keyboards.admin.confirmation_banners import confirmation_banners_kb
from keyboards.admin.general_menu_admin_kb import general_menu_admins_kb
from keyboards.admin.inline_admin_kb import kb_upload
from keyboards.admin.сonfirmation_promo import confirmation_promocode_kb

admin_router = Router()
admin_router.message.filter(ChatTypesFilter(['private']), IsAdmin())






class AddStockBasicBanners(StatesGroup):
    stock_name = State()
    data_zip = State()
    file_info = State()


class AddStockPromo(StatesGroup):
    stock_name = State()
    data_zip = State()
    file_info = State()



@admin_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Hello Admin!", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
    botlang = await get_botlang()
    botlang[message.chat.id] = 'en'
    await save_botlang(botlang)


@admin_router.message(F.text == "Upload")
async def uploadData(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Select what needs to be done:", reply_markup=kb_upload.as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data.startswith('action_'))
async def upload_process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    # Извлекаем данные из callback_data
    action = callback_query.data

    if action == 'action_add':
        # await callback_query.message.edit_reply_markup(reply_markup=None)
        # Отправляем ответ пользователю
        await callback_query.message.answer("Select what to add:",
                                            reply_markup=await admin_add_stock_menu())
    elif action == 'action_change':
        await callback_query.message.edit_reply_markup(reply_markup=None)

    elif action == 'action_delete':
        await callback_query.message.edit_reply_markup(reply_markup=None)


@admin_router.callback_query(lambda c: c.data.startswith('add_stock_'))
async def upload_add_stock_process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    action = callback_query.data
    if action == "add_stock_basic_baner":
        await callback_query.message.answer("Please send the offer name (Basic banners):",
                                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.stock_name)
    elif action == "add_stock_promo":
        await callback_query.message.answer("Please send the offer name (Promo):",
                                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockPromo.stock_name)








@admin_router.message(AddStockBasicBanners.stock_name, F.text)
async def add_name_stock_basic_banner(message: types.Message, state: FSMContext):
    if message.text and re.match(r'^[A-Za-z0-9]+$', message.text):
        await state.update_data(stock_name=message.text)
        await message.answer("Select the availability of a promotional code for this promotion",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.data_zip)
    else:
        await message.answer("Enter the correct promotion name:",
                             reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.stock_name)









@admin_router.message(AddStockBasicBanners.data_zip, F.document)
async def handle_basic_banner_zip_file(message: types.Message, bot: Bot, state: FSMContext):
    # Проверка, что файл является ZIP архивом
    if not message.document.file_name.endswith('.zip'):
        await message.reply("Пожалуйста, отправьте ZIP-архив.", reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.set_state(AddStockBasicBanners.data_zip)
    else:
        LANGUAGES = ['az', 'uz', 'kz', 'tr', 'ru', 'en', 'br', 'ng']
        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg']

        # Загрузка архива
        file_info = await bot.get_file(message.document.file_id)
        await state.update_data(file_info=file_info.file_path)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Проверка наличия файлов нужного типа в архиве
        with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not any(file.lower().endswith(tuple(ALLOWED_EXTENSIONS)) for file in file_list):
                await message.reply(
                    "The archive does not contain supported files (JPEG). Please send an archive with JPEG images.",
                    reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
                await state.set_state(AddStockBasicBanners.data_zip)
            else:
                # Создание уникальной временной директории для распаковки
                temp_dir = os.path.join(".", f"temp_{message.chat.id}")
                os.makedirs(temp_dir, exist_ok=True)

                # Распаковка ZIP-архива
                zip_ref.extractall(temp_dir)

            # Группировка файлов по языковым окончаниям
            language_groups = {}
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    for lang in LANGUAGES:
                        if file.endswith(f'_{lang}.jpg') or file.endswith(f'_{lang}.jpeg'):  # Поддерживаемые форматы
                            relative_path = os.path.relpath(os.path.join(root, file), ".")
                            if lang not in language_groups:
                                language_groups[lang] = []
                            language_groups[lang].append(relative_path)

            # Отправка файлов по группам
            for lang, files in language_groups.items():
                if files:
                    # Создание медиагруппы
                    media_group = MediaGroupBuilder()
                    data_state = await state.get_data()
                    if False:
                        await process_images_and_add_text(files, "TEST", (100, 100))

                    for file_path in files:
                        media_group.add_photo(media=FSInputFile(file_path))

                    # Отправка медиагруппы
                    first_media = media_group.build()[0] if media_group.build() else None
                    caption = f"{lang.upper()}"
                    if first_media:
                        first_media.caption = caption

                    await bot.send_media_group(
                        chat_id=message.chat.id,
                        media=media_group.build()
                    )
                    await asyncio.sleep(1/3)


            await message.answer("Add banners?", reply_markup=await confirmation_banners_kb())

            # Удаление временной директории и её содержимого
            shutil.rmtree(temp_dir)
            await state.set_state(AddStockBasicBanners.file_info)





@admin_router.callback_query(AddStockBasicBanners.file_info, lambda c: c.data.startswith('confirmation_banners_'))
async def upload_confirmation_banners_process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    action = callback_query.data
    banners = {
        "basic_banners": {
        }
    }
    if action == 'confirmation_banners_remake':
        await callback_query.message.answer("Select what to add:",
                                            reply_markup=await admin_add_stock_menu())
        await state.clear()

    elif action == 'confirmation_banners_apply':
        data = await state.get_data()
        downloaded_file = await bot.download_file(data['file_info'])
        os.makedirs(os.path.join('stock_data', 'basic_banners', data['stock_name']), exist_ok=True)

        main_folder_path = os.path.join("stock_data", "basic_banners", data['stock_name'])

        with zipfile.ZipFile(downloaded_file) as archive:
            for file_name in archive.namelist():
                if '_' in file_name:
                    # Определение типа промо
                    if '_promo_' in file_name:
                        promo_type = 'promo'
                    else:
                        promo_type = 'no_promo'

                    # Извлечение языка (после последнего '_')
                    suffix = file_name.split('_')[-1].split('.')[0]
                    language = suffix  # Язык находится в конце имени файла перед расширением

                    # Создание папки для языка и типа промо
                    folder_path = os.path.join(main_folder_path, language, promo_type)
                    os.makedirs(folder_path, exist_ok=True)

                    # Определение имени файла без путей
                    file_name_without_path = os.path.basename(file_name)

                    # Полный путь для извлечения
                    extract_path = os.path.join(folder_path, file_name_without_path)

                    # Извлечение файла
                    with open(extract_path, 'wb') as out_file:
                        out_file.write(archive.read(file_name))
        print(banners)
        await callback_query.message.reply(f"Promotion {data['stock_name']} added successfully!",
                            reply_markup=general_menu_admins_kb.as_markup(resize_keyboard=True))
        await state.clear()




